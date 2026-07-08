import frappe

def remove_analytics_tab():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    doc.fields = [f for f in doc.fields if f.fieldname != "analytics_tab"]
    
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Removed analytics_tab.")
    frappe.destroy()

if __name__ == "__main__":
    remove_analytics_tab()
