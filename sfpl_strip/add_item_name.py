import frappe

def add_item_name():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Yarn Data")
    if not any(f.fieldname == "item_name" for f in doc.fields):
        doc.append("fields", {
            "fieldname": "item_name",
            "fieldtype": "Data",
            "label": "Yarn Name",
            "fetch_from": "yarn.item_name",
            "read_only": 1,
            "in_list_view": 1
        })
        
        # Sort so item_name is immediately after yarn
        order = ["yarn", "item_name", "denier", "number_of_yarn", "denier_strength"]
        doc.fields.sort(key=lambda x: order.index(x.fieldname) if x.fieldname in order else 999)
        
        for i, f in enumerate(doc.fields):
            f.idx = i + 1
            
        doc.save(ignore_permissions=True)
        print("Added item_name field.")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    add_item_name()
