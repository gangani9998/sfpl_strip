import frappe

def fix_total_fields():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    has_total_yarn = any(f.fieldname == "total_yarn_weight" for f in doc.fields)
    has_total_coating = any(f.fieldname == "total_coating_weight" for f in doc.fields)
    
    if not has_total_yarn:
        doc.append("fields", {
            "fieldname": "total_yarn_weight",
            "fieldtype": "Float",
            "label": "Total Yarn Weight (kg)",
            "read_only": 1
        })
        
    if not has_total_coating:
        doc.append("fields", {
            "fieldname": "total_coating_weight",
            "fieldtype": "Float",
            "label": "Total Coating Weight (kg)",
            "read_only": 1
        })
        
    # Re-order so they appear after coating_details
    coating_idx = 0
    for i, f in enumerate(doc.fields):
        if f.fieldname == "coating_details":
            coating_idx = f.idx
            break
            
    # Set the newly appended fields idx
    for f in doc.fields:
        if f.fieldname == "total_yarn_weight":
            f.idx = coating_idx + 0.1
        elif f.fieldname == "total_coating_weight":
            f.idx = coating_idx + 0.2
            
    # Sort doc.fields by idx
    doc.fields.sort(key=lambda x: x.idx)
    
    # Re-assign sequential integer idx
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Fixed total weight fields.")
    frappe.destroy()

if __name__ == "__main__":
    fix_total_fields()
