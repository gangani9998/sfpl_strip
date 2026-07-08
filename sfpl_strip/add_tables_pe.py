import frappe

def update_production_entry():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    # Remove old float fields
    doc.fields = [f for f in doc.fields if f.fieldname not in ["yarn_weight", "coating_weight"]]
    
    # Find the index of bom_tab
    bom_idx = 0
    for i, f in enumerate(doc.fields):
        if f.fieldname == "bom_tab":
            bom_idx = i
            break
            
    # Insert Table fields after bom_tab
    yarn_field = frappe.get_doc({
        "doctype": "DocField",
        "fieldname": "yarn_details",
        "fieldtype": "Table",
        "label": "Yarn Details",
        "options": "Strip Production Yarn"
    })
    
    coating_field = frappe.get_doc({
        "doctype": "DocField",
        "fieldname": "coating_details",
        "fieldtype": "Table",
        "label": "Coating Details",
        "options": "Strip Production Coating"
    })
    
    # We will just append them, Frappe handles sorting by idx if we don't care, 
    # but let's insert them right after bom_tab
    doc.fields.insert(bom_idx + 1, yarn_field)
    doc.fields.insert(bom_idx + 2, coating_field)
    
    # Re-calculate idx
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Added child tables to Strip Production Entry.")
    frappe.destroy()

if __name__ == "__main__":
    update_production_entry()
