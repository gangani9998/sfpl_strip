import frappe

def run():
    if not frappe.db.exists("Print Format", "MTC Strip"):
        pf = frappe.new_doc("Print Format")
        pf.name = "MTC Strip"
        pf.doc_type = "MTC Strip"
        pf.module = "SFPL Strip"
        pf.custom_format = 1
        pf.print_format_builder = 0
        pf.standard = "Yes"
        pf.html = "<h1>Test</h1>"
        pf.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Created Print Format")
    else:
        print("Already exists")
