# Copyright (c) 2026, Jay Kumar Gangani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StripWorkSchedule(Document):
    def validate(self):
        self.validate_single_active_constraint()
        self.validate_coating_ratios()
        self.validate_targets()
        self.validate_wastage_requirement()
        self.check_mtc_gate()

    def validate_wastage_requirement(self):
        if self.get("workflow_state") == "Job Complete":
            # Check if there are any submitted production entries
            has_production = frappe.db.exists("Strip Production Entry", {"strip_work_schedule": self.name, "docstatus": 1})
            if has_production:
                total_wastage = sum([frappe.utils.flt(row.wastage_qty) for row in self.get("wastage_entries")])
                if total_wastage <= 0:
                    frappe.throw("Wastage is compulsory. You must log wastage entry since Production Entries exist for this schedule.")

    def on_cancel(self):
        # Prevent cancellation if there are active Production Entries
        if frappe.db.exists("Strip Production Entry", {"strip_work_schedule": self.name, "docstatus": ["!=", 2]}):
            frappe.throw("Cannot cancel Work Schedule because there are active Production Entries linked to it.")
            
    def before_cancel(self):
        has_production = frappe.db.exists("Strip Production Entry", {"strip_work_schedule": self.name, "docstatus": ["<", 2]})
        if has_production:
            frappe.throw("Cannot cancel this Work Schedule because Production Entries have already been created against it.")
            
        total_wastage = sum([frappe.utils.flt(row.wastage_qty) for row in self.get("wastage_entries")])
        if total_wastage > 0:
            frappe.throw("Cannot cancel this Work Schedule because Wastage has been permanently logged and/or posted.")

    def before_amend(self):
        frappe.throw("Amendments are strictly disabled for Strip Work Schedules. Use the 'Re-Production' workflow action instead.")

    def validate_targets(self):
        if frappe.utils.flt(self.target_qty) <= 0:
            frappe.throw("Target Qty (Meters) must be greater than zero.")
        if frappe.utils.flt(self.roll_size) <= 0:
            frappe.throw("Roll Size (Meters) must be greater than zero.")
        if frappe.utils.flt(self.target_gsm) <= 0:
            frappe.throw("Target GLM must be greater than zero.")

    def validate_coating_ratios(self):
        if self.default_coating_ratios:
            total_ratio = sum([frappe.utils.flt(row.ratio) for row in self.default_coating_ratios])
            if total_ratio != 100.0:
                frappe.throw(f"Total Coating Ratio must be exactly 100%. Currently it is {total_ratio}%")
    def validate_single_active_constraint(self):
        if self.get("workflow_state") in ["Drawing", "Under Production"]:
            existing = frappe.get_all(
                "Strip Work Schedule",
                filters={
                    "extrusion_line": self.extrusion_line,
                    "workflow_state": ["in", ["Drawing", "Under Production"]],
                    "name": ["!=", self.name]
                }
            )
            if existing:
                frappe.throw(f"Extrusion Line {self.extrusion_line} is already occupied by another Work Schedule in Drawing/Production state.")
                
        # Validate that if status is Job Complete, there must be wastage recorded (if needed)
    def check_mtc_gate(self):
        if self.get("workflow_state") == "Job Complete":
            # Just a placeholder for MTC gate check, will expand when MTCs are built
            pass

    def onload(self):
        self.update_production_analysis()
        
    def on_update(self):
        # Only runs for Draft documents
        pass

    def on_update_after_submit(self):
        if self.get("workflow_state") == "Job Complete":
            self.validate_wastage_requirement()
            if not self.wastage_posted:
                self.post_wastage_entry()
            else:
                old_doc = self.get_doc_before_save()
                if old_doc:
                    old_wastage = sum([frappe.utils.flt(row.wastage_qty) for row in old_doc.get("wastage_entries")])
                    new_wastage = sum([frappe.utils.flt(row.wastage_qty) for row in self.get("wastage_entries")])
                    if old_wastage != new_wastage:
                        frappe.throw("Wastage Log cannot be modified because the Job is Complete and Stock Entries have already been generated.")
            
    def post_wastage_entry(self):
        # 1. Calculate total wastage
        total_wastage = sum([frappe.utils.flt(row.wastage_qty) for row in self.get("wastage_entries")])
        if total_wastage <= 0:
            return
            
        if not self.wastage_item:
            frappe.throw("Cannot post wastage. Please select a Wastage/Scrap Item on the Work Schedule.")
            
        if not frappe.db.get_value("Item", self.wastage_item, "is_stock_item"):
            frappe.throw(f"Wastage Item '{self.wastage_item}' must be marked as 'Maintain Stock' in the Item Master to generate Stock Entries.")
            
        # 2. Get all RM usage from Production Entries
        entries = frappe.get_all("Strip Production Entry", 
            filters={"strip_work_schedule": self.name, "docstatus": 1}
        )
        
        rm_usage = {}
        total_rm_weight = 0.0
        
        if not entries:
            # THEORETICAL DEDUCTION ENGINE
            target_glm = frappe.utils.flt(self.target_gsm)
            if target_glm <= 0:
                frappe.throw("Target GLM must be set to calculate theoretical wastage.")
            
            # 1. Yarn Weight per meter (kg/m)
            yarn_kg_per_m = 0.0
            if self.warp_data:
                for row in self.warp_data:
                    weight = (frappe.utils.flt(row.denier) * frappe.utils.flt(row.number_of_yarn) * 0.0001111) / 1000
                    yarn_kg_per_m += weight
                    rm_usage[row.yarn] = rm_usage.get(row.yarn, 0.0) + weight
            
            # 2. Coating Weight per meter (kg/m)
            target_kg_per_m = target_glm / 1000
            coating_kg_per_m = target_kg_per_m - yarn_kg_per_m
            if coating_kg_per_m < 0:
                coating_kg_per_m = 0.0
                
            if self.default_coating_ratios:
                for row in self.default_coating_ratios:
                    weight = coating_kg_per_m * (frappe.utils.flt(row.ratio) / 100)
                    rm_usage[row.coating_material] = rm_usage.get(row.coating_material, 0.0) + weight
                    
            total_rm_weight = sum(rm_usage.values())
        else:
            for e in entries:
                pe = frappe.get_doc("Strip Production Entry", e.name)
                for yarn in pe.get("yarn_details"):
                    if frappe.utils.flt(yarn.weight) > 0:
                        rm_usage[yarn.yarn] = rm_usage.get(yarn.yarn, 0.0) + frappe.utils.flt(yarn.weight)
                        total_rm_weight += frappe.utils.flt(yarn.weight)
                        
                for coating in pe.get("coating_details"):
                    if frappe.utils.flt(coating.weight) > 0:
                        rm_usage[coating.coating_material] = rm_usage.get(coating.coating_material, 0.0) + frappe.utils.flt(coating.weight)
                        total_rm_weight += frappe.utils.flt(coating.weight)
                        
        if total_rm_weight <= 0:
            frappe.throw("Cannot post wastage because calculated RM weight is zero.")
            
        # 3. Generate Stock Entry (Repack)
        default_warehouse = frappe.db.get_single_value("Stock Settings", "default_warehouse")
        if not default_warehouse:
            frappe.throw("Please set a Default Warehouse in Stock Settings.")
            
        se = frappe.new_doc("Stock Entry")
        se.stock_entry_type = "Repack"
        se.purpose = "Repack"
        se.company = frappe.defaults.get_user_default("Company")
        se.from_warehouse = default_warehouse
        se.to_warehouse = default_warehouse
        
        # Add RM deductions based on precise percentage of total usage
        for item_code, weight in rm_usage.items():
            ratio = weight / total_rm_weight
            wastage_deduction = total_wastage * ratio
            
            if wastage_deduction > 0:
                se.append("items", {
                    "item_code": item_code,
                    "qty": wastage_deduction,
                    "s_warehouse": default_warehouse,
                    "is_finished_item": 0
                })
                
        # Add Output Scrap Item
        se.append("items", {
            "item_code": self.wastage_item,
            "qty": total_wastage,
            "t_warehouse": default_warehouse,
            "is_finished_item": 1
        })
        
        se.insert(ignore_permissions=True)
        se.submit()
        
        # Mark as posted
        self.db_set("wastage_posted", 1)

    def update_production_analysis(self):
        entries = frappe.get_all("Strip Production Entry", 
            filters={"strip_work_schedule": self.name, "docstatus": ["<", 2]},
            fields=["name", "docstatus", "roll_length", "total_yarn_weight", "total_coating_weight", "roll_net_weight", "gsm"]
        )
        
        submitted_meter = 0.0
        draft_meter = 0.0
        
        total_yarn = 0.0
        total_coating = 0.0
        total_net_weight = 0.0
        total_gsm = 0.0
        
        for e in entries:
            length = frappe.utils.flt(e.roll_length)
            yarn = frappe.utils.flt(e.total_yarn_weight)
            coating = frappe.utils.flt(e.total_coating_weight)
            net = frappe.utils.flt(e.roll_net_weight)
            gsm = frappe.utils.flt(e.gsm)
            
            if e.docstatus == 1:
                submitted_meter += length
            elif e.docstatus == 0:
                draft_meter += length
                
            total_yarn += yarn
            total_coating += coating
            total_net_weight += net
            total_gsm += gsm
            
        total_produced_meter = submitted_meter + draft_meter
        target_meter = frappe.utils.flt(self.target_qty)
        remain_meter = target_meter - total_produced_meter
        total_roll = len(entries)
        
        self.batch_production_meter = target_meter
        self.submitted_production_meter = submitted_meter
        self.draft_production_meter = draft_meter
        self.total_produced_meter = total_produced_meter
        self.remain_production_meter = remain_meter
        self.total_roll = total_roll
        
        # Calculate Yarn Coating Ratio (e.g., 90:10) based on actual totals
        if total_net_weight > 0:
            yarn_pct = round((total_yarn / total_net_weight) * 100)
            coating_pct = 100 - yarn_pct
            self.yarn_coating_ratio = f"{yarn_pct}:{coating_pct}"
        else:
            self.yarn_coating_ratio = "0:0"
            
        if total_roll > 0:
            self.average_gsm = total_gsm / total_roll
        else:
            self.average_gsm = 0.0
            
        # If it's loaded, we shouldn't save unless it changed, but onload doesn't save to DB.
        # To persist this, we also call this method from Strip Production Entry's hooks.
