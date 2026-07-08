import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def fix_item_links():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # 1. Remove the hacky item_name field
    doc = frappe.get_doc("DocType", "Strip Yarn Data")
    doc.fields = [f for f in doc.fields if f.fieldname != "item_name"]
    doc.save(ignore_permissions=True)
    
    # 2. Make Item links show title (item_name)
    make_property_setter("Item", None, "show_title_field_in_link", "1", "Check")
    
    frappe.db.commit()
    print("Fixed item links to show name instead of ID.")
    frappe.destroy()

if __name__ == "__main__":
    fix_item_links()
