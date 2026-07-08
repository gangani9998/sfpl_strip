import frappe

def remove_permlevel():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    changed = False
    for field in doc.fields:
        if field.permlevel == 1:
            field.permlevel = 0
            changed = True
            
    if changed:
        doc.save(ignore_permissions=True)
        print("Removed permlevel from Setup fields.")
    else:
        print("No fields with permlevel 1 found.")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    remove_permlevel()
