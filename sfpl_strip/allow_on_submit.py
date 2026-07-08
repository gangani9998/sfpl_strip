import frappe

def allow_on_submit():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    fields_to_allow = [
        "batch_production_meter",
        "submitted_production_meter",
        "draft_production_meter",
        "total_produced_meter",
        "remain_production_meter",
        "total_roll",
        "average_gsm",
        "yarn_coating_ratio"
    ]
    
    modified = False
    for f in doc.fields:
        if f.fieldname in fields_to_allow:
            if not f.allow_on_submit:
                f.allow_on_submit = 1
                modified = True
                
    if modified:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Enabled allow_on_submit for analysis fields.")
    else:
        print("Already allowed on submit.")
        
    frappe.destroy()

if __name__ == "__main__":
    allow_on_submit()
