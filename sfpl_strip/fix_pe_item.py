import frappe

def fix_pe_item():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    changed = False
    for f in doc.fields:
        if f.fieldname == "strip_product_code":
            if not f.read_only or f.fetch_from != "strip_work_schedule.quality":
                f.read_only = 1
                f.fetch_from = "strip_work_schedule.quality"
                changed = True
                
    if changed:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Updated strip_product_code in Strip Production Entry.")
        
    frappe.destroy()

if __name__ == "__main__":
    fix_pe_item()
