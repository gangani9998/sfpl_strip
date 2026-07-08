import frappe

def adjust_layout():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    modified = False
    
    # 1. Swap Wastage Qty and Wastage Entries
    qty_idx = 0
    entries_idx = 0
    for f in doc.fields:
        if f.fieldname == "wastage_qty":
            qty_idx = f.idx
        if f.fieldname == "wastage_entries":
            entries_idx = f.idx
            
    if qty_idx < entries_idx:
        for f in doc.fields:
            if f.fieldname == "wastage_qty":
                f.idx = entries_idx + 0.1
                modified = True
                break
                
    # 2. Add Column Breaks in Coating Data to put items side-by-side
    has_cb1 = any(f.fieldname == "col_break_coating_1" for f in doc.fields)
    has_cb2 = any(f.fieldname == "col_break_coating_2" for f in doc.fields)
    
    table_idx = 0
    for f in doc.fields:
        if f.fieldname == "default_coating_ratios":
            table_idx = f.idx
            break
            
    if not has_cb1:
        doc.append("fields", {
            "fieldname": "col_break_coating_1",
            "fieldtype": "Column Break",
            "insert_after": "default_coating_ratios"
        })
        modified = True
        
    if not has_cb2:
        doc.append("fields", {
            "fieldname": "col_break_coating_2",
            "fieldtype": "Column Break",
            "insert_after": "default_paper_tube"
        })
        modified = True
        
    if modified:
        # Sort to assign proper idx
        # We need to manually set idx for the new column breaks
        for f in doc.fields:
            if f.fieldname == "col_break_coating_1":
                f.idx = table_idx + 0.1
            elif f.fieldname == "default_paper_tube":
                f.idx = table_idx + 0.2
            elif f.fieldname == "col_break_coating_2":
                f.idx = table_idx + 0.3
            elif f.fieldname == "wastage_item":
                f.idx = table_idx + 0.4
                
        doc.fields.sort(key=lambda x: getattr(x, 'idx', 999))
        for i, f in enumerate(doc.fields):
            f.idx = i + 1
            
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Adjusted layout: Swapped wastage fields and added column breaks for side-by-side items.")
    else:
        print("Layout already adjusted.")
        
    frappe.destroy()

if __name__ == "__main__":
    adjust_layout()
