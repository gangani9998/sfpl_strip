import frappe

def show_wastage_section():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    modified = False
    for f in doc.fields:
        if f.fieldname == "wastage_section":
            if f.depends_on:
                f.depends_on = None
                modified = True
                
    if modified:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Removed depends_on from wastage_section.")
    else:
        print("wastage_section is already visible.")
        
    frappe.destroy()

if __name__ == "__main__":
    show_wastage_section()
