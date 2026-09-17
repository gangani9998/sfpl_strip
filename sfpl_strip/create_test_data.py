import frappe

def create():
    # 1. Create Item Groups
    groups = ["GeoStrap", "Pack Strap"]
    for g in groups:
        if not frappe.db.exists("Item Group", g):
            doc = frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": g,
                "parent_item_group": "All Item Groups"
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Item Group: {g}")
            
    # 2. Create Items
    items = [
        {"item_code": "TEST-GEOSTRAP", "item_name": "Test GeoStrap", "item_group": "GeoStrap"},
        {"item_code": "TEST-PACKSTRAP", "item_name": "Test Pack Strap", "item_group": "Pack Strap"}
    ]
    
    for i in items:
        if not frappe.db.exists("Item", i["item_code"]):
            doc = frappe.get_doc({
                "doctype": "Item",
                "item_code": i["item_code"],
                "item_name": i["item_name"],
                "item_group": i["item_group"],
                "stock_uom": "Nos",
                "is_stock_item": 1
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Item: {i['item_code']}")
            
    frappe.db.commit()
    print("Test data created successfully.")

