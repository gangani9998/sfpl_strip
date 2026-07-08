import frappe

def move_paper_tube():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    target_idx = 0
    for f in doc.fields:
        if f.fieldname == "target_qty":
            target_idx = f.idx
            break
            
    for f in doc.fields:
        if f.fieldname == "default_paper_tube":
            f.idx = target_idx - 0.5
            break
            
    doc.fields.sort(key=lambda x: x.idx)
    
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Moved Paper Tube to above Planned Production.")
    frappe.destroy()

if __name__ == "__main__":
    move_paper_tube()
