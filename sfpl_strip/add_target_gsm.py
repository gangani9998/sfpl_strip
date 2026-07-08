import frappe

def add_target_gsm():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    if not any(f.fieldname == "target_gsm" for f in doc.fields):
        doc.append("fields", {
            "fieldname": "target_gsm",
            "fieldtype": "Float",
            "label": "Target GSM",
            "reqd": 1,
            "insert_after": "roll_size"
        })
        
        # Sort so it's after roll_size
        order = [
            "schedule_section",
            "extrusion_line",
            "quality",
            "target_qty",
            "roll_size",
            "target_gsm",
            "column_break_schedule",
            "warp_data_section",
            "warp_data",
            "strip_tensile_strength",
            "default_coating_ratios",
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
        print("Added Target GSM field.")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    add_target_gsm()
