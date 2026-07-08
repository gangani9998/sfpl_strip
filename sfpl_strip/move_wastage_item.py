import frappe

def move_and_enforce_wastage_item():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    modified = False
    
    # Get idx of default_paper_tube
    paper_tube_idx = 0
    for f in doc.fields:
        if f.fieldname == "default_paper_tube":
            paper_tube_idx = f.idx
            break
            
    for f in doc.fields:
        if f.fieldname == "wastage_item":
            f.reqd = 1
            f.allow_on_submit = 0
            f.idx = paper_tube_idx + 0.5
            modified = True
            break
            
    if modified:
        doc.fields.sort(key=lambda x: getattr(x, 'idx', 999))
        for i, f in enumerate(doc.fields):
            f.idx = i + 1
            
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Moved wastage_item, made it compulsory, and removed allow_on_submit.")
    else:
        print("No changes made.")
        
    frappe.destroy()

if __name__ == "__main__":
    move_and_enforce_wastage_item()
