import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def add_bom_tab():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    # Check if bom_tab already exists
    if not any(f.fieldname == "bom_tab" for f in doc.fields):
        # We will append the Tab Break and fields at the end of the form
        doc.append("fields", {
            "fieldname": "bom_tab",
            "fieldtype": "Tab Break",
            "label": "BOM"
        })
        
        doc.append("fields", {
            "fieldname": "yarn_weight",
            "fieldtype": "Float",
            "label": "Yarn Weight (kg)",
            "read_only": 1
        })
        
        doc.append("fields", {
            "fieldname": "coating_weight",
            "fieldtype": "Float",
            "label": "Coating Weight (kg)",
            "read_only": 1
        })
        
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Added BOM tab and fields to Strip Production Entry.")
    else:
        print("Fields already exist.")
        
    frappe.destroy()

if __name__ == "__main__":
    add_bom_tab()
