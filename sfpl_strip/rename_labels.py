import frappe

def rename_wastage_labels():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    modified = False
    for f in doc.fields:
        if f.fieldname == "wastage_section":
            f.label = "Log Event Wastage"
            modified = True
        elif f.fieldname == "wastage_qty":
            f.label = "Total Wastage Quantity (Kg)"
            modified = True
            
    if modified:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Renamed wastage section and qty labels.")
    else:
        print("Labels already matched.")
        
    frappe.destroy()

if __name__ == "__main__":
    rename_wastage_labels()
