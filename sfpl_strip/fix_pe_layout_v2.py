import frappe

def fix_layout():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    new_order = [
        "naming_series",
        "strip_work_schedule",
        "strip_product_code",
        "col_break_1",
        "posting_date",
        "posting_time",
        "barcode",
        "batch_no"
    ]
    
    # Set the idx property for all fields
    current_idx = 1
    
    # First, the fields in new_order
    for fieldname in new_order:
        for f in doc.fields:
            if f.fieldname == fieldname:
                f.idx = current_idx
                current_idx += 1
                break
                
    # Then the rest of the fields
    for f in doc.fields:
        if f.fieldname not in new_order:
            f.idx = current_idx
            current_idx += 1
            
    # Sort the doc.fields array by the new idx
    doc.fields.sort(key=lambda x: x.idx)
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Fixed layout for Strip Production Entry.")
    frappe.destroy()

if __name__ == "__main__":
    fix_layout()
