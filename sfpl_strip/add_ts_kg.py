import frappe

def add_ts_kg():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    if not any(f.fieldname == "strip_tensile_strength_kg" for f in doc.fields):
        doc.append("fields", {
            "fieldname": "strip_tensile_strength_kg",
            "fieldtype": "Float",
            "label": "Strip Tensile Strength (kg)",
            "read_only": 1,
            "insert_after": "strip_tensile_strength"
        })
        
        # Sort to ensure it is immediately after strip_tensile_strength
        order = [
            "schedule_section",
            "extrusion_line",
            "quality",
            "column_break_schedule",
            "die_no",
            "sizer_no",
            "warp_data_section",
            "warp_data",
            "strip_tensile_strength",
            "strip_tensile_strength_kg",
            "default_coating_ratios",
            "target_qty",
            "roll_size",
            "target_gsm",
            "wastage_section",
            "wastage_item",
            "wastage_qty"
        ]
        
        for f in doc.fields:
            if f.fieldname not in order:
                order.append(f.fieldname)
                
        doc.fields.sort(key=lambda x: order.index(x.fieldname))
        
        for i, f in enumerate(doc.fields):
            f.idx = i + 1
            
        doc.save(ignore_permissions=True)
        print("Added Strip Tensile Strength (kg).")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    add_ts_kg()
