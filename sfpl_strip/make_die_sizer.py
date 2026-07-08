import frappe

def create_doctypes():
    frappe.init(site="site1.localhost")
    frappe.connect()

    if not frappe.db.exists("DocType", "Die"):
        doc = frappe.new_doc("DocType")
        doc.name = "Die"
        doc.module = "SFPL Strip"
        doc.custom = 1
        doc.autoname = "field:die_name"
        doc.append("fields", {
            "fieldname": "die_name",
            "fieldtype": "Data",
            "label": "Die Name",
            "reqd": 1,
            "unique": 1
        })
        doc.insert(ignore_permissions=True)
        print("Created Die doctype.")

    if not frappe.db.exists("DocType", "Sizer"):
        doc = frappe.new_doc("DocType")
        doc.name = "Sizer"
        doc.module = "SFPL Strip"
        doc.custom = 1
        doc.autoname = "field:sizer_name"
        doc.append("fields", {
            "fieldname": "sizer_name",
            "fieldtype": "Data",
            "label": "Sizer Name",
            "reqd": 1,
            "unique": 1
        })
        doc.insert(ignore_permissions=True)
        print("Created Sizer doctype.")
        
    sws = frappe.get_doc("DocType", "Strip Work Schedule")
    changed = False
    for f in sws.fields:
        if f.fieldname == "die_no":
            f.fieldtype = "Link"
            f.options = "Die"
            changed = True
        if f.fieldname == "sizer_no":
            f.fieldtype = "Link"
            f.options = "Sizer"
            changed = True
            
    if changed:
        sws.save(ignore_permissions=True)
        print("Updated fields to Link in Strip Work Schedule.")
        
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    create_doctypes()
