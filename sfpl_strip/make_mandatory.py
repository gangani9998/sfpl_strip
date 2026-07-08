import frappe

def make_mandatory():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    changed = False
    
    for f in doc.fields:
        if f.fieldname in ["die_no", "sizer_no"]:
            if not f.reqd:
                f.reqd = 1
                changed = True
                
    if changed:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Made Die No and Sizer No mandatory.")
        
    frappe.destroy()

if __name__ == "__main__":
    make_mandatory()
