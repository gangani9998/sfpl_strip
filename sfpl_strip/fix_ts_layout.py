import frappe

def fix_ts_layout():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    # We want to re-order the fields array to ensure they are:
    # section_break_ts -> strip_tensile_strength -> column_break_ts -> strip_tensile_strength_kg
    
    new_fields = []
    ts_fields = ["section_break_ts", "strip_tensile_strength", "column_break_ts", "strip_tensile_strength_kg"]
    
    # Remove these fields from their current positions
    extracted = {}
    for f in list(doc.fields):
        if f.fieldname in ts_fields:
            extracted[f.fieldname] = f
            doc.fields.remove(f)
            
    # Find warp_data
    insert_idx = 0
    for i, f in enumerate(doc.fields):
        if f.fieldname == "warp_data":
            insert_idx = i + 1
            break
            
    # Insert them in the correct order
    for fname in ts_fields:
        if fname in extracted:
            doc.fields.insert(insert_idx, extracted[fname])
            insert_idx += 1
            
    # Re-calculate idx
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Fixed layout for Strip Work Schedule Tensile Strength fields.")
    frappe.destroy()

if __name__ == "__main__":
    fix_ts_layout()
