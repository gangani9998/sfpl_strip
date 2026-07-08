import frappe

def cleanup_permissions():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # Find duplicates in tabDocPerm
    perms = frappe.get_all("DocPerm", filters={"parent": "Strip Work Schedule"}, fields=["name", "role", "permlevel", "if_owner"], order_by="idx")
    
    seen = set()
    to_delete = []
    
    for p in perms:
        key = (p.role, p.permlevel, p.if_owner)
        if key in seen:
            to_delete.append(p.name)
        else:
            seen.add(key)
            
    print(f"Found {len(to_delete)} duplicate permissions.")
    
    for name in to_delete:
        print(f"Deleting duplicate perm {name}")
        frappe.delete_doc("DocPerm", name, force=1)
        
    frappe.db.commit()
    
    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    doc.custom=0
    doc.save(ignore_permissions=True)
    
    frappe.db.commit()
    print("Done cleaning permissions and syncing JSON.")
    frappe.destroy()

if __name__ == "__main__":
    cleanup_permissions()
