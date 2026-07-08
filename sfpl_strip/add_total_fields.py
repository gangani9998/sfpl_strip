import frappe

def add_total_fields():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    # Check if fields already exist
    has_total_yarn = any(f.fieldname == "total_yarn_weight" for f in doc.fields)
    has_total_coating = any(f.fieldname == "total_coating_weight" for f in doc.fields)
    
    # Find the index of the last child table to insert after
    insert_idx = len(doc.fields)
    for i, f in enumerate(doc.fields):
        if f.fieldname == "coating_details":
            insert_idx = i + 1
            break
            
    if not has_total_yarn:
        total_yarn_field = frappe.get_doc({
            "doctype": "DocField",
            "fieldname": "total_yarn_weight",
            "fieldtype": "Float",
            "label": "Total Yarn Weight (kg)",
            "read_only": 1
        })
        doc.fields.insert(insert_idx, total_yarn_field)
        insert_idx += 1
        
    if not has_total_coating:
        total_coating_field = frappe.get_doc({
            "doctype": "DocField",
            "fieldname": "total_coating_weight",
            "fieldtype": "Float",
            "label": "Total Coating Weight (kg)",
            "read_only": 1
        })
        doc.fields.insert(insert_idx, total_coating_field)
        
    # Re-calculate idx
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Added Total Weight fields back to Strip Production Entry.")
    frappe.destroy()

if __name__ == "__main__":
    add_total_fields()
