import frappe

def remove_setup_fields():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    to_remove = ["setup_section", "default_yarn_item", "column_break_setup", "default_paper_tube"]
    
    doc.fields = [f for f in doc.fields if f.fieldname not in to_remove]
    doc.save(ignore_permissions=True)
    
    frappe.db.commit()
    print("Successfully removed the setup fields.")
    frappe.destroy()

if __name__ == "__main__":
    remove_setup_fields()
