import frappe

def fix_layout():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    # Desired order for the first section:
    # Left column: naming_series, strip_work_schedule, strip_product_code
    # col_break_1
    # Right column: posting_date, posting_time, qr_code, batch_no
    
    # We will just reorder the fields list
    new_order = [
        "naming_series",
        "strip_work_schedule",
        "strip_product_code",
        "col_break_1",
        "posting_date",
        "posting_time",
        "qr_code",
        "batch_no"
    ]
    
    # Get all fields not in new_order (the rest of the fields)
    rest_of_fields = [f.fieldname for f in doc.fields if f.fieldname not in new_order]
    
    # Combine the lists
    final_order = new_order + rest_of_fields
    
    # Create a dictionary of fields
    field_dict = {f.fieldname: f for f in doc.fields}
    
    # Clear and re-append in correct order
    doc.fields = []
    for fn in final_order:
        doc.append("fields", field_dict[fn])
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Fixed layout for Strip Production Entry.")
    frappe.destroy()

if __name__ == "__main__":
    fix_layout()
