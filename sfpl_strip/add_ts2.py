import frappe

def add_ts():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    if not any(f.fieldname == "strip_tensile_strength" for f in doc.fields):
        doc.append("fields", {
            "fieldname": "strip_tensile_strength",
            "fieldtype": "Float",
            "label": "Strip Tensile Strength (kN)",
            "read_only": 1,
            "insert_after": "warp_data"
        })
        doc.save(ignore_permissions=True)
        print("Added")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    add_ts()
