import frappe

def fix_fields():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    # Remove production_status
    doc.fields = [f for f in doc.fields if f.fieldname != "production_status"]
    
    # Desired order
    order = [
        "schedule_section",
        "extrusion_line",
        "quality",
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
    frappe.db.commit()
    print("Fixed layout and removed production_status.")
    frappe.destroy()

if __name__ == "__main__":
    fix_fields()
