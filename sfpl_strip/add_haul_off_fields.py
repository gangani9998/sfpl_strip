import frappe

def add_fields():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    has_temp = any(f.fieldname == "haul_off_temp" for f in doc.fields)
    has_follower = any(f.fieldname == "haul_off_follower_rpm" for f in doc.fields)
    
    if not has_temp:
        doc.append("fields", {
            "fieldname": "haul_off_temp",
            "fieldtype": "Float",
            "label": "Haul-Off Temp",
            "insert_after": "haul_off_rpm"
        })
        
    if not has_follower:
        doc.append("fields", {
            "fieldname": "haul_off_follower_rpm",
            "fieldtype": "Float",
            "label": "Haul-Off Follower RPM",
            "insert_after": "haul_off_temp"
        })
        
    # Re-sort using frappe's insert_after logic if we want, or manually set idx
    # Let's manually set idx based on haul_off_rpm
    base_idx = 0
    for f in doc.fields:
        if f.fieldname == "haul_off_rpm":
            base_idx = f.idx
            break
            
    for f in doc.fields:
        if f.fieldname == "haul_off_temp":
            f.idx = base_idx + 0.1
        elif f.fieldname == "haul_off_follower_rpm":
            f.idx = base_idx + 0.2
            
    doc.fields.sort(key=lambda x: x.idx)
    
    for i, f in enumerate(doc.fields):
        f.idx = i + 1

    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Added Haul-Off fields.")
    frappe.destroy()

if __name__ == "__main__":
    add_fields()
