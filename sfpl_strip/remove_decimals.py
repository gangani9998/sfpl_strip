import frappe

def remove_decimals():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # 1. Update Strip Work Schedule fields
    doc_ws = frappe.get_doc("DocType", "Strip Work Schedule")
    ws_fields_to_change = [
        "target_qty",
        "roll_size",
        "batch_production_meter",
        "submitted_production_meter",
        "draft_production_meter",
        "total_produced_meter",
        "remain_production_meter"
    ]
    
    modified_ws = False
    for f in doc_ws.fields:
        if f.fieldname in ws_fields_to_change:
            if f.fieldtype != "Int":
                f.fieldtype = "Int"
                modified_ws = True
                print(f"Changed {f.fieldname} to Int in Strip Work Schedule")
                
    if modified_ws:
        doc_ws.save(ignore_permissions=True)

    # 2. Update Strip Production Entry fields
    doc_pe = frappe.get_doc("DocType", "Strip Production Entry")
    modified_pe = False
    for f in doc_pe.fields:
        if f.fieldname == "roll_length":
            if f.fieldtype != "Int":
                f.fieldtype = "Int"
                modified_pe = True
                print(f"Changed {f.fieldname} to Int in Strip Production Entry")
                
    if modified_pe:
        doc_pe.save(ignore_permissions=True)

    if modified_ws or modified_pe:
        frappe.db.commit()
        print("Successfully removed decimals from meter fields.")
    else:
        print("Fields are already Int.")

    frappe.destroy()

if __name__ == "__main__":
    remove_decimals()
