import frappe

def fix_target_qty_label():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    changed = False
    for f in doc.fields:
        if f.fieldname == "target_qty":
            f.label = "Target Qty (Meters)"
            changed = True
            
    if changed:
        doc.save(ignore_permissions=True)
        print("Updated Target Qty label to Meters.")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    fix_target_qty_label()
