import frappe

def add_paper_tube_field():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    if not any(f.fieldname == "default_paper_tube" for f in doc.fields):
        # Insert after roll_size
        doc.append("fields", {
            "fieldname": "default_paper_tube",
            "fieldtype": "Link",
            "options": "Item",
            "label": "Paper Tube (Packing Material)",
            "insert_after": "roll_size"
        })
        
        # Sort manually
        idx_offset = 0
        for f in doc.fields:
            if f.fieldname == "roll_size":
                idx_offset = f.idx
                break
                
        for f in doc.fields:
            if f.fieldname == "default_paper_tube":
                f.idx = idx_offset + 0.5
                
        doc.fields.sort(key=lambda x: x.idx)
        
        for i, f in enumerate(doc.fields):
            f.idx = i + 1
            
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Added Paper Tube field.")
    else:
        print("Field already exists.")
        
    frappe.destroy()

if __name__ == "__main__":
    add_paper_tube_field()
