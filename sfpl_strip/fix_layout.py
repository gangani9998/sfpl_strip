import frappe

def fix_layout():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    if not any(f.fieldname == "column_break_ts" for f in doc.fields):
        doc.append("fields", {
            "fieldname": "column_break_ts",
            "fieldtype": "Column Break"
        })
        
    if not any(f.fieldname == "section_break_coating" for f in doc.fields):
        doc.append("fields", {
            "fieldname": "section_break_coating",
            "fieldtype": "Section Break",
            "label": "Coating Data"
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
        "column_break_ts",
        "strip_tensile_strength_kg",
        "section_break_coating",
        "default_coating_ratios",
        "target_qty",
        "roll_size",
        "target_gsm",
        "wastage_section",
        "wastage_item",
        "wastage_qty",
        "amended_from"
    ]
    
    doc.fields.sort(key=lambda x: order.index(x.fieldname) if x.fieldname in order else 999)
    
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Fixed layout.")
    frappe.destroy()

if __name__ == "__main__":
    fix_layout()
