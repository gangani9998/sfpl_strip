import frappe

def add_gsm_field():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    if not any(f.fieldname == "gsm" for f in doc.fields):
        # We want to add it under the BOM tab.
        # Find bom_tab index
        bom_idx = 0
        for f in doc.fields:
            if f.fieldname == "bom_tab":
                bom_idx = f.idx
                break
                
        # Insert after bom_tab
        doc.append("fields", {
            "fieldname": "gsm",
            "fieldtype": "Float",
            "label": "GSM (g/m)",
            "read_only": 1,
            "insert_after": "bom_tab"
        })
        
        # Sort manually
        for f in doc.fields:
            if f.fieldname == "gsm":
                f.idx = bom_idx + 0.5
                
        doc.fields.sort(key=lambda x: x.idx)
        
        for i, f in enumerate(doc.fields):
            f.idx = i + 1
            
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Added GSM field to Production Entry.")
    else:
        print("GSM field already exists.")
        
    frappe.destroy()

if __name__ == "__main__":
    add_gsm_field()
