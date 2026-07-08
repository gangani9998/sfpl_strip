import frappe

def reorder_fields():
    frappe.init(site="site1.localhost")
    frappe.connect()
    
    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    order = [
        "schedule_section",
        "extrusion_line",
        "quality",
        "column_break_schedule",
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
    
    for f in doc.fields:
        if f.fieldname not in order:
            order.append(f.fieldname)
            
    doc.fields.sort(key=lambda x: order.index(x.fieldname))
    
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Reordered fields correctly.")
    frappe.destroy()

if __name__ == "__main__":
    reorder_fields()
