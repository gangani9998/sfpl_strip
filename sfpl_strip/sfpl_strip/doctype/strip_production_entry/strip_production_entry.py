# Copyright (c) 2026, Jay Kumar Gangani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
import qrcode
from io import BytesIO
from frappe.utils.file_manager import save_file

class StripProductionEntry(Document):
    def validate(self):
        if self.strip_work_schedule and self.is_new():
            ws = frappe.get_doc("Strip Work Schedule", self.strip_work_schedule)
            if ws.docstatus != 1 or ws.workflow_state not in ["Under Production", "Under production"]:
                frappe.throw(f"Production Entries can only be created against Work Schedules that are 'Under Production'. The selected Work Schedule {ws.name} is currently '{ws.workflow_state}'.")
                
        if flt(self.roll_gross_weight) > 50:
            frappe.throw("Roll Gross Weight cannot be greater than 50 kg.")
            
        if flt(self.roll_gross_weight) < 1:
            frappe.throw("Roll Gross Weight cannot be less than 1 kg.")
                
        if (flt(self.total_packaging_weight) / 1000) >= flt(self.roll_gross_weight):
            frappe.throw("Total Packaging Weight cannot be greater than or equal to Roll Gross Weight.")
            
        if flt(self.actual_strip_width) > 100:
            frappe.throw("Actual Strip Width (mm) cannot be greater than 100 mm.")

        self.calculate_weights()
            
    def calculate_weights(self):
        """Calculate net weight and meters"""
        # Net Weight = Gross - Packaging (now packaging is in grams)
        if self.roll_gross_weight and self.total_packaging_weight is not None:
            self.roll_net_weight = flt(self.roll_gross_weight) - (flt(self.total_packaging_weight) / 1000)
            
    def on_update(self):
        # Generate Barcode value on first save (when name is available)
        if not self.barcode and self.name:
            # Frappe natively converts the string to an SVG barcode visually
            self.db_set('barcode', self.name)
        
        self.update_work_schedule_analysis()
            
    def on_submit(self):
        self.db_set("remaining_length", flt(self.roll_length))
        self.db_set("remaining_weight", flt(self.roll_net_weight))
        self.create_batch()
        self.make_manufacturing_entry()
        self.update_work_schedule_analysis()

    def on_cancel(self):
        self.update_work_schedule_analysis()
        
    def after_delete(self):
        self.update_work_schedule_analysis()
        
    def update_work_schedule_analysis(self):
        if self.strip_work_schedule and frappe.db.exists("Strip Work Schedule", self.strip_work_schedule):
            ws = frappe.get_doc("Strip Work Schedule", self.strip_work_schedule)
            ws.update_production_analysis(save=True)

    def create_batch(self):
        # Ensure the Item is configured for batches
        item_doc = frappe.get_doc("Item", self.strip_product_code)
        if not item_doc.has_batch_no:
            item_doc.has_batch_no = 1
            item_doc.save(ignore_permissions=True)
            
        if not frappe.db.exists("Batch", self.name):
            batch = frappe.new_doc("Batch")
            batch.batch_id = self.name
            batch.item = self.strip_product_code
            batch.strip_work_schedule = self.strip_work_schedule
            batch.strip_production_entry = self.name
            batch.insert(ignore_permissions=True)

    def make_manufacturing_entry(self):
        ws = frappe.get_doc("Strip Work Schedule", self.strip_work_schedule)
        
        # 2. Create Stock Entry
        se = frappe.new_doc("Stock Entry")
        se.stock_entry_type = "Manufacture"
        se.purpose = "Manufacture" # Keeping purpose for legacy compatibility if needed
        se.strip_production_entry = self.name
        se.company = frappe.defaults.get_user_default("Company")
        
        default_warehouse = frappe.db.get_single_value("Stock Settings", "default_warehouse")
        if not default_warehouse:
            frappe.throw("Please set a Default Warehouse in Stock Settings.")
            
        se.from_warehouse = default_warehouse
        se.to_warehouse = default_warehouse
        
        # Deduction: Paper Tube
        if ws.default_paper_tube:
            se.append("items", {
                "item_code": ws.default_paper_tube,
                "qty": 1,
                "s_warehouse": default_warehouse,
                "is_finished_item": 0
            })
            
        # Deduction: Yarn (Dynamic from child table)
        for yarn in (self.get("yarn_details") or []):
            if yarn.weight > 0:
                se.append("items", {
                    "item_code": yarn.yarn,
                    "qty": yarn.weight,
                    "s_warehouse": default_warehouse,
                    "is_finished_item": 0
                })
            
        # Deduction: Coating (Dynamic from child table)
        for coating in (self.get("coating_details") or []):
            if coating.weight > 0:
                se.append("items", {
                    "item_code": coating.coating_material,
                    "qty": coating.weight,
                    "s_warehouse": default_warehouse,
                    "is_finished_item": 0
                })
            
        company = frappe.defaults.get_user_default("Company")
        company_abbr = frappe.get_cached_value("Company", company, "abbr")
        
        target_warehouse = default_warehouse
        if self.flag_for_qc:
            target_warehouse = f"QC Hold - {company_abbr}"

        # Addition: Finished Good
        se.append("items", {
            "item_code": self.strip_product_code,
            "qty": flt(self.roll_length),
            "t_warehouse": target_warehouse,
            "is_finished_item": 1,
            "batch_no": self.name
        })
        
        se.insert(ignore_permissions=True)
        se.submit()

@frappe.whitelist()
def make_sample_cut(entry_name, sample_length, purpose):
    import frappe
    from frappe.utils import flt
    
    doc = frappe.get_doc("Strip Production Entry", entry_name)
    sample_length = flt(sample_length)
    
    if sample_length <= 0:
        frappe.throw("Sample Length must be greater than 0")
        
    if sample_length > flt(doc.remaining_length):
        frappe.throw(f"Sample length ({sample_length} m) cannot exceed the remaining length of the roll ({doc.remaining_length} m).")
        
    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Issue"
    se.purpose = "Material Issue"
    se.company = frappe.defaults.get_user_default("Company")
    
    default_warehouse = frappe.db.get_single_value("Stock Settings", "default_warehouse")
    if not default_warehouse:
        frappe.throw("Please set a Default Warehouse in Stock Settings.")
        
    if purpose == "Lab Testing":
        expense_account = "Lab Testing - SFPL"
    else:
        expense_account = "Marketing Expenses - SFPL"
        
    company_doc = frappe.get_cached_doc("Company", se.company)
    cost_center = company_doc.cost_center or frappe.defaults.get_user_default("Cost Center")
        
    se.append("items", {
        "item_code": doc.strip_product_code,
        "qty": sample_length,
        "s_warehouse": default_warehouse,
        "batch_no": doc.name,
        "expense_account": expense_account,
        "cost_center": cost_center
    })
    
    se.insert(ignore_permissions=True)
    se.submit()
    
    new_remaining_length = flt(doc.remaining_length) - sample_length
    
    if doc.gsm:
        new_remaining_weight = (new_remaining_length * flt(doc.gsm)) / 1000.0
    else:
        new_remaining_weight = 0
        
    doc.db_set("remaining_length", new_remaining_length)
    doc.db_set("remaining_weight", new_remaining_weight)
    
    return se.name

@frappe.whitelist()
def process_qc_scrap(entry_name, scrap_length, defect_reason):
    import frappe
    from frappe.utils import flt
    
    doc = frappe.get_doc("Strip Production Entry", entry_name)
    scrap_length = flt(scrap_length)
    
    if scrap_length <= 0:
        frappe.throw("Scrap Length must be greater than 0")
        
    if scrap_length > flt(doc.remaining_length):
        frappe.throw(f"Scrap length ({scrap_length} m) cannot exceed the remaining length of the roll ({doc.remaining_length} m).")
        
    ws = frappe.get_doc("Strip Work Schedule", doc.strip_work_schedule)
    wastage_item = ws.get("wastage_item")
    if not wastage_item:
        frappe.throw(f"No Wastage Item defined in the Strip Work Schedule ({ws.name}). Please set one to process scrap.")
        
    default_warehouse = frappe.db.get_single_value("Stock Settings", "default_warehouse")
    company = frappe.defaults.get_user_default("Company")
    company_abbr = frappe.get_cached_value("Company", company, "abbr")
    quarantine_warehouse = f"QC Hold - {company_abbr}"
    
    # 1. Repack Scrap
    se_repack = frappe.new_doc("Stock Entry")
    se_repack.stock_entry_type = "Repack"
    se_repack.purpose = "Repack"
    se_repack.company = company
    
    # Issue Finished Good from QC
    se_repack.append("items", {
        "item_code": doc.strip_product_code,
        "qty": scrap_length,
        "s_warehouse": quarantine_warehouse,
        "batch_no": doc.name
    })
    
    # Receive Wastage Item into QC
    se_repack.append("items", {
        "item_code": wastage_item,
        "qty": scrap_length,
        "t_warehouse": quarantine_warehouse,
        "is_finished_item": 1
    })
    
    se_repack.insert(ignore_permissions=True)
    se_repack.submit()
    
    new_remaining_length = flt(doc.remaining_length) - scrap_length
    
    # 2. Material Transfer for Remaining Good Length (if any left)
    if new_remaining_length > 0:
        se_transfer = frappe.new_doc("Stock Entry")
        se_transfer.stock_entry_type = "Material Transfer"
        se_transfer.purpose = "Material Transfer"
        se_transfer.company = company
        
        se_transfer.append("items", {
            "item_code": doc.strip_product_code,
            "qty": new_remaining_length,
            "s_warehouse": quarantine_warehouse,
            "t_warehouse": default_warehouse,
            "batch_no": doc.name
        })
        se_transfer.insert(ignore_permissions=True)
        se_transfer.submit()
    
    if doc.gsm:
        new_remaining_weight = (new_remaining_length * flt(doc.gsm)) / 1000.0
    else:
        new_remaining_weight = 0
        
    doc.db_set("remaining_length", new_remaining_length)
    doc.db_set("remaining_weight", new_remaining_weight)
    doc.db_set("flag_for_qc", 0) # Clear the flag
    
    # Optionally save the defect reason to a note or comment on the document
    if defect_reason:
        frappe.get_doc({
            "doctype": "Comment",
            "comment_type": "Info",
            "reference_doctype": "Strip Production Entry",
            "reference_name": doc.name,
            "content": f"<b>QC Processed:</b> {scrap_length}m scrapped. Reason: {defect_reason}"
        }).insert(ignore_permissions=True)
    
    return True
