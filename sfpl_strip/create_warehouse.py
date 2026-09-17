import frappe

def create():
    companies = frappe.get_all("Company", pluck="name")
    
    for company in companies:
        parent = frappe.db.get_value("Warehouse", {"is_group": 1, "company": company}, "name")
        if not parent:
            continue
            
        abbr = frappe.get_cached_value("Company", company, "abbr")
        warehouse_name = f"QC Hold - {abbr}"
        
        if not frappe.db.exists("Warehouse", warehouse_name):
            w = frappe.new_doc("Warehouse")
            w.warehouse_name = "QC Hold"
            w.parent_warehouse = parent
            w.company = company
            w.insert(ignore_permissions=True)
            print(f"Created QC Hold - {abbr} for {company}")
        else:
            print(f"QC Hold - {abbr} already exists for {company}")
