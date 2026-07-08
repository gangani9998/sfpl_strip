import frappe

def add_fields():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    if not any(f.fieldname == "die_no" for f in doc.fields):
        doc.append("fields", {
            "fieldname": "die_no",
            "fieldtype": "Data",
            "label": "Die No"
        })
        
    if not any(f.fieldname == "sizer_no" for f in doc.fields):
        doc.append("fields", {
            "fieldname": "sizer_no",
            "fieldtype": "Data",
            "label": "Sizer No"
        })
        
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
        "default_coating_ratios",
        "target_qty",
        "roll_size",
        "target_gsm",
        "wastage_section",
        "wastage_item",
        "wastage_qty"
    ]
    
    doc.fields.sort(key=lambda x: order.index(x.fieldname) if x.fieldname in order else 999)
    
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Added die_no and sizer_no.")
    frappe.destroy()

if __name__ == "__main__":
    add_fields()
