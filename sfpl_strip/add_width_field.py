import frappe

def add_width_field():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    if not any(f.fieldname == "strip_width_mm" for f in doc.fields):
        # Insert after roll_length
        doc.append("fields", {
            "fieldname": "strip_width_mm",
            "fieldtype": "Float",
            "label": "Strip Width (mm)",
            "insert_after": "roll_length",
            "reqd": 1
        })
        
        # Sort manually
        idx_offset = 0
        for f in doc.fields:
            if f.fieldname == "roll_length":
                idx_offset = f.idx
                break
                
        for f in doc.fields:
            if f.fieldname == "strip_width_mm":
                f.idx = idx_offset + 0.5
                
        doc.fields.sort(key=lambda x: x.idx)
        
        for i, f in enumerate(doc.fields):
            f.idx = i + 1
            
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Added Strip Width (mm) field.")
    else:
        print("Field already exists.")
        
    frappe.destroy()

if __name__ == "__main__":
    add_width_field()
