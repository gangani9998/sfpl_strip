import frappe

def backfill_wastage_totals():
    frappe.init(site="site1.localhost")
    frappe.connect()

    schedules = frappe.get_all("Strip Work Schedule", fields=["name"])
    
    for s in schedules:
        doc = frappe.get_doc("Strip Work Schedule", s.name)
        total = sum([frappe.utils.flt(row.wastage_qty) for row in doc.get("wastage_entries")])
        if total > 0 and frappe.utils.flt(doc.wastage_qty) != total:
            # We don't want to trigger validations if it's already Job Complete
            frappe.db.set_value("Strip Work Schedule", s.name, "wastage_qty", total)
            print(f"Updated {s.name} total to {total}")
            
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    backfill_wastage_totals()
