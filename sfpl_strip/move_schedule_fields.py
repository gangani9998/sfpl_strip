import frappe

def move_fields():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    modified = False
    
    # Target indices
    quality_idx = 0
    sizer_idx = 0
    
    for f in doc.fields:
        if f.fieldname == "quality":
            quality_idx = f.idx
        if f.fieldname == "sizer_no":
            sizer_idx = f.idx
            
    for f in doc.fields:
        if f.fieldname == "target_qty":
            f.idx = quality_idx + 0.1
            modified = True
        elif f.fieldname == "roll_size":
            f.idx = quality_idx + 0.2
            modified = True
        elif f.fieldname == "target_gsm":
            f.idx = sizer_idx + 0.1
            modified = True
            
    if modified:
        doc.fields.sort(key=lambda x: getattr(x, 'idx', 999))
        for i, f in enumerate(doc.fields):
            f.idx = i + 1
            
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Moved target_qty, roll_size, and target_gsm to Work Schedule section.")
    else:
        print("Fields already moved.")
        
    frappe.destroy()

if __name__ == "__main__":
    move_fields()
