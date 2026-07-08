import frappe

def fix_table_layout():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    modified = False
    for f in doc.fields:
        if f.fieldname == "col_break_coating_1":
            f.fieldtype = "Section Break"
            f.label = ""
            # Maybe rename the fieldname to avoid confusion, but not strictly necessary.
            modified = True
            break
            
    if modified:
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Changed col_break_coating_1 to a Section Break to fix table width.")
    else:
        print("No changes made.")
        
    frappe.destroy()

if __name__ == "__main__":
    fix_table_layout()
