import frappe

def revert_decimals():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # Revert Strip Production Entry roll_length back to Float
    doc_pe = frappe.get_doc("DocType", "Strip Production Entry")
    modified_pe = False
    for f in doc_pe.fields:
        if f.fieldname == "roll_length":
            f.fieldtype = "Float"
            modified_pe = True
                
    if modified_pe:
        doc_pe.save(ignore_permissions=True)
        print("Reverted roll_length to Float")

    # Revert all bottom dashboard sum fields in Strip Work Schedule back to Float
    doc_ws = frappe.get_doc("DocType", "Strip Work Schedule")
    ws_fields_to_change = [
        "batch_production_meter",
        "submitted_production_meter",
        "draft_production_meter",
        "total_produced_meter",
        "remain_production_meter"
    ]
    
    modified_ws = False
    for f in doc_ws.fields:
        if f.fieldname in ws_fields_to_change:
            f.fieldtype = "Float"
            modified_ws = True
                
    if modified_ws:
        doc_ws.save(ignore_permissions=True)
        print("Reverted bottom dashboard meter fields to Float")

    if modified_ws or modified_pe:
        frappe.db.commit()

    frappe.destroy()

if __name__ == "__main__":
    revert_decimals()
