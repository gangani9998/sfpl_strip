import frappe

def remove_batch_no():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    # Remove the batch_no field
    doc.fields = [f for f in doc.fields if f.fieldname != "batch_no"]
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Removed batch_no field from Strip Production Entry.")
    frappe.destroy()

if __name__ == "__main__":
    remove_batch_no()
