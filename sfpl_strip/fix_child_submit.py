import frappe

def fix_child_table_submit():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Wastage Entry")
    
    modified = False
    for f in doc.fields:
        if not f.allow_on_submit:
            f.allow_on_submit = 1
            modified = True
            
    if modified:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Set allow_on_submit=1 for Strip Wastage Entry fields.")
    else:
        print("Already set.")
        
    frappe.destroy()

if __name__ == "__main__":
    fix_child_table_submit()
