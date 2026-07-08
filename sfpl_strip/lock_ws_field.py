import frappe

def lock_ws_field():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    for f in doc.fields:
        if f.fieldname == "strip_work_schedule":
            f.read_only = 1
            f.set_only_once = 1
            
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Locked strip_work_schedule field.")
    frappe.destroy()

if __name__ == "__main__":
    lock_ws_field()
