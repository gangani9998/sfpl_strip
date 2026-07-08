import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def add_creation_logs():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # Add custom fields to DocType (actually, let's just modify the JSON directly via DocType to make it core)
    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    # Check if created_on exists
    if not any(f.fieldname == "created_on" for f in doc.fields):
        # Insert after extrusion_line
        idx = 0
        for i, f in enumerate(doc.fields):
            if f.fieldname == "extrusion_line":
                idx = i
                break
                
        doc.insert("fields", {
            "fieldname": "created_on",
            "label": "Created On",
            "fieldtype": "Datetime",
            "read_only": 1,
            "in_list_view": 1
        }, idx + 1)
        
        doc.insert("fields", {
            "fieldname": "created_by",
            "label": "Created By",
            "fieldtype": "Data",
            "read_only": 1,
            "in_list_view": 1
        }, idx + 2)
        
        doc.save(ignore_permissions=True)
        print("Added created_on and created_by fields to Strip Work Schedule")
        
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    add_creation_logs()
