import frappe

def move_width():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    posting_idx = 0
    for f in doc.fields:
        if f.fieldname == "posting_time":
            posting_idx = f.idx
            break
            
    for f in doc.fields:
        if f.fieldname == "strip_width_mm":
            f.idx = posting_idx + 0.5
            break
            
    doc.fields.sort(key=lambda x: x.idx)
    
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Moved Strip Width to below posting time.")
    frappe.destroy()

if __name__ == "__main__":
    move_width()
