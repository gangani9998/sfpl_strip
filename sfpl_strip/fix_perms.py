import frappe

def fix_perms():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    # Check if level 1 perm already exists
    has_level_1 = any(p.permlevel == 1 and p.role == "System Manager" for p in doc.permissions)
    if not has_level_1:
        doc.append("permissions", {
            "role": "System Manager",
            "permlevel": 1,
            "read": 1,
            "write": 1,
            "create": 0,
            "delete": 0,
            "submit": 0
        })
        doc.save(ignore_permissions=True)
        print("Added level 1 permissions for System Manager.")
    
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    fix_perms()
