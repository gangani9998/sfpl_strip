import frappe

def make_ro_again():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    for f in doc.fields:
        if f.fieldname == "roll_net_weight":
            f.read_only = 1
            
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Made roll_net_weight read_only=1 again.")
    frappe.destroy()

if __name__ == "__main__":
    make_ro_again()
