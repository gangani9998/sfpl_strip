import frappe

def fix_allow_on_submit():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    modified = False
    for f in doc.fields:
        if f.fieldname in ("wastage_item", "wastage_qty", "wastage_entries", "wastage_posted"):
            if not f.allow_on_submit:
                f.allow_on_submit = 1
                modified = True
                
    if modified:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Set allow_on_submit=1 for wastage fields.")
    else:
        print("Already set.")
        
    frappe.destroy()

if __name__ == "__main__":
    fix_allow_on_submit()
