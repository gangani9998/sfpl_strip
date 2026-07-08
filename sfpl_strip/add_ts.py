import frappe

def add_tensile_strength():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    if not any(f.fieldname == "tensile_strength" for f in doc.fields):
        # find index of warp_data to place it right after
        idx = next((i for i, f in enumerate(doc.fields) if f.fieldname == "warp_data"), -1)
        if idx != -1:
            doc.fields.insert(idx + 1, frappe._dict({
                "fieldname": "tensile_strength",
                "fieldtype": "Float",
                "label": "Tensile Strength (kN)",
                "read_only": 1
            }))
            doc.save(ignore_permissions=True)
            print("Added Tensile Strength field.")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    add_tensile_strength()
