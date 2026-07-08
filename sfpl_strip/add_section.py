import frappe

def add_warp_data_section():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    # Check if section break exists
    if not any(f.fieldname == "warp_data_section" for f in doc.fields):
        # find index of warp_data
        idx = next((i for i, f in enumerate(doc.fields) if f.fieldname == "warp_data"), -1)
        if idx != -1:
            doc.fields.insert(idx, frappe._dict({
                "fieldname": "warp_data_section",
                "fieldtype": "Section Break",
                "label": "Warp Data"
            }))
            doc.save(ignore_permissions=True)
            print("Added section break for Warp Data.")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    add_warp_data_section()
