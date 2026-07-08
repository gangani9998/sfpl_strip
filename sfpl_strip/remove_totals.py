import frappe

def remove_totals():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    to_remove = ["total_production", "total_roll_count"]
    doc.fields = [f for f in doc.fields if f.fieldname not in to_remove]
    
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Removed total_production and total_roll_count.")
    frappe.destroy()

if __name__ == "__main__":
    remove_totals()
