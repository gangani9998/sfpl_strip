import frappe

def add_target_qty():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    if not any(f.fieldname == "target_qty" for f in doc.fields):
        doc.append("fields", {
            "fieldname": "target_qty",
            "fieldtype": "Float",
            "label": "Target Qty (kg)",
            "reqd": 1,
            "insert_after": "quality"
        })
        
        # Sort so target_qty is immediately after quality
        # order: schedule_section, extrusion_line, quality, target_qty, column_break_schedule...
        order = [
            "schedule_section",
            "extrusion_line",
            "quality",
            "target_qty",
            "column_break_schedule",
            "warp_data_section",
            "warp_data",
            "strip_tensile_strength",
            "default_coating_ratios",
            "analytics_tab",
            "total_production",
            "total_roll_count",
            "wastage_section",
            "wastage_item",
            "wastage_qty"
        ]
        
        doc.fields.sort(key=lambda x: order.index(x.fieldname) if x.fieldname in order else 999)
        
        for i, f in enumerate(doc.fields):
            f.idx = i + 1
            
        doc.save(ignore_permissions=True)
        print("Added Target Qty field.")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    add_target_qty()
