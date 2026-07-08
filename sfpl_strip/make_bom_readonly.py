import frappe

def make_bom_tables_read_only():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    modified = False
    for f in doc.fields:
        if f.fieldname in ["yarn_details", "coating_details"]:
            if not f.read_only:
                f.read_only = 1
                modified = True
                
    if modified:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Set BOM tables to read-only.")
    else:
        print("Already read-only.")
        
    frappe.destroy()

if __name__ == "__main__":
    make_bom_tables_read_only()
