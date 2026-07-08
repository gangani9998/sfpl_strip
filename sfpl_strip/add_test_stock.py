import frappe

def add_test_stock():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # Get items to add stock for (Yarns, Raw Materials, Packing Materials)
    items = frappe.get_all("Item", 
        filters={
            "item_group": ["in", ["Yarn", "Raw Material", "Packing Material"]],
            "is_stock_item": 1
        },
        fields=["name"]
    )
    
    if not items:
        print("No raw materials found.")
        return

    company = frappe.defaults.get_user_default("Company") or frappe.get_all("Company")[0].name
    default_warehouse = frappe.db.get_single_value("Stock Settings", "default_warehouse")
    
    if not default_warehouse:
        print("No default warehouse set in Stock Settings!")
        return

    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Receipt"
    se.company = company
    
    for item in items:
        se.append("items", {
            "item_code": item.name,
            "qty": 10000,
            "t_warehouse": default_warehouse,
            "basic_rate": 100 # arbitrary valuation rate
        })
        
    se.insert(ignore_permissions=True)
    se.submit()
    frappe.db.commit()
    print(f"Successfully added 10,000 unit test stock for {len(items)} items in Stock Entry: {se.name}")

    frappe.destroy()

if __name__ == "__main__":
    add_test_stock()
