import frappe

def trigger_wastage():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("Strip Work Schedule", "SWS-2026-00007")
    
    print("Calling post_wastage_entry...")
    doc.post_wastage_entry()
    print("Finished.")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    trigger_wastage()
