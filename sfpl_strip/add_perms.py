import frappe

def add_perms():
    frappe.init(site="site1.localhost")
    frappe.connect()

    for dt in ["Die", "Sizer"]:
        doc = frappe.get_doc("DocType", dt)
        
        # Avoid duplicating permissions if they exist
        has_sys_mgr = any(p.role == "System Manager" for p in doc.permissions)
        
        if not has_sys_mgr:
            doc.append("permissions", {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "export": 1,
                "report": 1
            })
            
            # Allow all users to read
            doc.append("permissions", {
                "role": "All",
                "read": 1
            })
            
            doc.save(ignore_permissions=True)
            print(f"Added permissions for {dt}.")

    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    add_perms()
