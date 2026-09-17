import requests
import frappe

def create():
    url = "https://erp.shivoham.tech/api/resource/Item"
    headers = {
        "Authorization": "token 54cd3cba3400d6d:beb13b452346ce7"
    }
    
    # Let's search exactly for Packstrap items
    response = requests.get(url, headers=headers, params={"limit_page_length": 500, "fields": '["item_code","item_name","item_group"]'})
    if response.status_code == 200:
        items = response.json().get("data", [])
        pack_items = [i for i in items if "Pack" in str(i.get("item_group", "")) or "Pack" in str(i.get("item_code", "")) or "PACK" in str(i.get("item_code", ""))]
        geo_items = [i for i in items if "Geo" in str(i.get("item_group", "")) or "Strip" in str(i.get("item_group", ""))]
        
        for item in (pack_items[:3] + geo_items[:3]):
            item_code = item["item_code"]
            item_group = item.get("item_group", "Products")
            
            if not frappe.db.exists("Item Group", item_group):
                frappe.get_doc({
                    "doctype": "Item Group",
                    "item_group_name": item_group,
                    "parent_item_group": "All Item Groups"
                }).insert(ignore_permissions=True)
                
            if not frappe.db.exists("Item", item_code):
                frappe.get_doc({
                    "doctype": "Item",
                    "item_code": item_code,
                    "item_name": item.get("item_name", item_code),
                    "item_group": item_group,
                    "stock_uom": "Nos",
                    "is_stock_item": 1
                }).insert(ignore_permissions=True)
                print(f"Created: {item_code} ({item_group})")
            else:
                frappe.db.set_value("Item", item_code, "item_group", item_group)
                print(f"Updated: {item_code} to {item_group}")
                
        frappe.db.commit()
    else:
        print("Failed to fetch.")

