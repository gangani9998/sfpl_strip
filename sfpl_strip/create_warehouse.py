import frappe

def create():
    company = frappe.db.get_value("Company", {"name": ["like", "Shivoham%"]}, "name")
    parent = frappe.db.get_value("Warehouse", {"is_group": 1}, "name")
    abbr = frappe.get_cached_value("Company", company, "abbr")
    
    if not frappe.db.exists("Warehouse", f"QC Hold - {abbr}"):
        w = frappe.new_doc("Warehouse")
        w.warehouse_name = "QC Hold"
        w.parent_warehouse = parent
        w.company = company
        w.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"Created QC Hold - {abbr}")
    else:
        print(f"QC Hold - {abbr} already exists")
