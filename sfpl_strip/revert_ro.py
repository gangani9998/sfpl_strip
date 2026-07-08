import frappe

def revert_read_only():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    for f in doc.fields:
        if f.fieldname == "roll_net_weight":
            f.read_only = 0
            
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Reverted read-only.")
    frappe.destroy()

if __name__ == "__main__":
    revert_read_only()
