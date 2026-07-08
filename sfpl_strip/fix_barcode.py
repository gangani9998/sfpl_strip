import frappe

def fix_barcode():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    # We will rename the qr_code field to barcode and change its type
    for f in doc.fields:
        if f.fieldname == "qr_code":
            f.fieldname = "barcode"
            f.label = "Barcode"
            f.fieldtype = "Barcode"
            
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Changed qr_code to barcode.")
    frappe.destroy()

if __name__ == "__main__":
    fix_barcode()
