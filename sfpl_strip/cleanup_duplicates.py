import frappe

def cleanup_duplicates():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # Find duplicates directly in the database
    fields = frappe.get_all("DocField", filters={"parent": "Strip Work Schedule"}, fields=["name", "fieldname"], order_by="idx")
    
    seen = set()
    to_delete = []
    
    for f in fields:
        if f.fieldname in seen:
            to_delete.append(f.name)
        else:
            seen.add(f.fieldname)
            
    print(f"Found {len(to_delete)} duplicate fields.")
    
    for name in to_delete:
        print(f"Deleting duplicate field {name}")
        frappe.delete_doc("DocField", name, force=1)
        
    # Also clean up the JSON by exporting the cleaned doc
    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    # Actually wait, Frappe might not let us save if the in-memory doc still has duplicates. Let's just force a reload
    frappe.db.commit()
    
    # Reload and save to sync JSON
    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    doc.custom=0
    # Touch the modified timestamp so it writes the file
    doc.save(ignore_permissions=True)
    
    frappe.db.commit()
    print("Done cleaning duplicates and syncing JSON.")
    frappe.destroy()

if __name__ == "__main__":
    cleanup_duplicates()
