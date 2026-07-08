import frappe

def rename_label():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    for f in doc.fields:
        if f.fieldname == "barcode":
            f.label = "Roll No"
            
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Changed label of barcode to Roll No.")
    frappe.destroy()

if __name__ == "__main__":
    rename_label()
