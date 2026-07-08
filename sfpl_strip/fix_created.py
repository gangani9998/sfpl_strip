import frappe

def fix_fields():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # 1. Remove 'created_by' if it exists
    if frappe.db.exists("DocField", {"parent": "Strip Work Schedule", "fieldname": "created_by"}):
        frappe.delete_doc("DocField", frappe.db.get_value("DocField", {"parent": "Strip Work Schedule", "fieldname": "created_by"}, "name"))

    # 2. Move 'created_on' above 'die_no'
    # Find idx of die_no
    die_no_idx = frappe.db.get_value("DocField", {"parent": "Strip Work Schedule", "fieldname": "die_no"}, "idx")
    
    if die_no_idx:
        created_on_name = frappe.db.get_value("DocField", {"parent": "Strip Work Schedule", "fieldname": "created_on"}, "name")
        if created_on_name:
            doc = frappe.get_doc("DocField", created_on_name)
            doc.insert_after = "extrusion_line" # Place it after extrusion_line, which is right before die_no
            doc.save()

    # Sync to JSON
    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    doc.save()

    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    fix_fields()
