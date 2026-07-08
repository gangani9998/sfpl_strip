import frappe

def make_submittable():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    doc.is_submittable = 1
    
    if not any(f.fieldname == "amended_from" for f in doc.fields):
        doc.append("fields", {
            "fieldname": "amended_from",
            "fieldtype": "Link",
            "options": "Strip Work Schedule",
            "label": "Amended From",
            "read_only": 1,
            "print_hide": 1,
            "no_copy": 1
        })
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Made Strip Work Schedule submittable and added amended_from field.")
    frappe.destroy()

if __name__ == "__main__":
    make_submittable()
