import frappe

def fix_net_weight():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    changed = False
    
    for f in doc.fields:
        if f.fieldname == "roll_net_weight":
            if not f.read_only:
                f.read_only = 1
                changed = True
                
    if changed:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Made roll_net_weight read-only.")
        
    frappe.destroy()

if __name__ == "__main__":
    fix_net_weight()
