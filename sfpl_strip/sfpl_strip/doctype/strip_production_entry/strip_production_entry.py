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
            if ws.docstatus != 1 or ws.workflow_state != "Under Production":
                frappe.throw(f"Production Entries can only be created against Work Schedules that are 'Under Production'. The selected Work Schedule {ws.name} is currently '{ws.workflow_state}'.")
                
        # Fallback math (will be updated side-by-side with user)
        if not self.roll_net_weight:
            self.roll_net_weight = flt(self.roll_gross_weight) - flt(self.papertube_weight)
            
    def on_update(self):
        # Generate Barcode value on first save (when name is available)
        if not self.barcode and self.name:
            # Frappe natively converts the string to an SVG barcode visually
            self.db_set('barcode', self.name)
        
        self.update_work_schedule_analysis()
            
    def on_submit(self):
        self.create_batch()
        self.make_manufacturing_entry()
        self.update_work_schedule_analysis()

    def on_cancel(self):
        self.update_work_schedule_analysis()
        
    def on_trash(self):
        self.update_work_schedule_analysis()
        
    def update_work_schedule_analysis(self):
        if self.strip_work_schedule:
            ws = frappe.get_doc("Strip Work Schedule", self.strip_work_schedule)
            ws.update_production_analysis()
            # Disable validation on this background save to avoid triggering MTC or state logic errors
            ws.flags.ignore_validate = True
            ws.save(ignore_permissions=True)

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
            
        # Addition: Finished Good
        se.append("items", {
            "item_code": self.strip_product_code,
            "qty": flt(self.roll_length),
            "t_warehouse": default_warehouse,
            "is_finished_item": 1,
            "batch_no": self.name
        })
        
        se.insert(ignore_permissions=True)
        se.submit()
