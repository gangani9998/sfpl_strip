import frappe

def set_default():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    for f in doc.fields:
        if f.fieldname == "roll_net_weight":
            f.default = "0"
            f.read_only = 1
            
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Set default 0 to roll_net_weight")
    frappe.destroy()

if __name__ == "__main__":
    set_default()
