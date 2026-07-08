import frappe

def rename_gsm_to_glm():
    frappe.init(site="site1.localhost")
    frappe.connect()

    modified = False

    # 1. Update Strip Work Schedule
    doc_ws = frappe.get_doc("DocType", "Strip Work Schedule")
    for f in doc_ws.fields:
        if f.fieldname == "target_gsm":
            f.label = "Target GLM"
            modified = True
        elif f.fieldname == "average_gsm":
            f.label = "Average GLM"
            modified = True
            
    if modified:
        doc_ws.save(ignore_permissions=True)

    # 2. Update Strip Production Entry
    doc_pe = frappe.get_doc("DocType", "Strip Production Entry")
    modified_pe = False
    for f in doc_pe.fields:
        if f.fieldname == "gsm":
            f.label = "GLM (g/m)"
            modified_pe = True
            
    if modified_pe:
        doc_pe.save(ignore_permissions=True)
        
    if modified or modified_pe:
        frappe.db.commit()
        print("Renamed GSM to GLM in UI labels.")
    else:
        print("No labels to rename.")
        
    frappe.destroy()

if __name__ == "__main__":
    rename_gsm_to_glm()
