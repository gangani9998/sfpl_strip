import frappe

def fix_bom_tables():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    # Check if they exist
    has_yarn = any(f.fieldname == "yarn_details" for f in doc.fields)
    has_coating = any(f.fieldname == "coating_details" for f in doc.fields)
    
    if not has_yarn:
        doc.append("fields", {
            "fieldname": "yarn_details",
            "fieldtype": "Table",
            "label": "Yarn Details",
            "options": "Strip Production Yarn"
        })
        
    if not has_coating:
        doc.append("fields", {
            "fieldname": "coating_details",
            "fieldtype": "Table",
            "label": "Coating Details",
            "options": "Strip Production Coating"
        })
        
    # Order: bom_tab -> yarn_details -> coating_details -> total_yarn_weight -> total_coating_weight
    
    bom_idx = 0
    for i, f in enumerate(doc.fields):
        if f.fieldname == "bom_tab":
            bom_idx = f.idx
            break
            
    # set the idx explicitly relative to bom_tab
    for f in doc.fields:
        if f.fieldname == "yarn_details":
            f.idx = bom_idx + 0.1
        elif f.fieldname == "coating_details":
            f.idx = bom_idx + 0.2
        elif f.fieldname == "total_yarn_weight":
            f.idx = bom_idx + 0.3
        elif f.fieldname == "total_coating_weight":
            f.idx = bom_idx + 0.4
            
    # Sort
    doc.fields.sort(key=lambda x: x.idx)
    
    # Reassign integer index
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Fixed BOM tables and layout.")
    frappe.destroy()

if __name__ == "__main__":
    fix_bom_tables()
