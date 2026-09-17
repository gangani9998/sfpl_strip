import requests
import json
import frappe

def create():
    url = "https://erp.shivoham.tech/api/resource/Item"
    headers = {
        "Authorization": "token 54cd3cba3400d6d:beb13b452346ce7"
    }
    
    # Fetch some items
    response = requests.get(url, headers=headers, params={"limit_page_length": 50, "fields": '["item_code","item_name","item_group"]'})
    if response.status_code == 200:
        items = response.json().get("data", [])
        
        # Filter for GeoStrap or Packstrap or anything with strip
        geo_items = [i for i in items if "Geo" in str(i.get("item_group", "")) or "Geo" in str(i.get("item_code", ""))]
        pack_items = [i for i in items if "Pack" in str(i.get("item_group", "")) or "Pack" in str(i.get("item_code", ""))]
        
        if not geo_items:
            geo_items = items[:2]
        if not pack_items:
            pack_items = items[2:4]
            
        selected_items = geo_items[:2] + pack_items[:2]
        
        for item in selected_items:
            item_code = item["item_code"]
            item_group = item.get("item_group", "Products")
            
            # Create item group if not exists
            if not frappe.db.exists("Item Group", item_group):
                frappe.get_doc({
                    "doctype": "Item Group",
                    "item_group_name": item_group,
                    "parent_item_group": "All Item Groups"
                }).insert(ignore_permissions=True)
                print(f"Created Item Group: {item_group}")
                
            if not frappe.db.exists("Item", item_code):
                frappe.get_doc({
                    "doctype": "Item",
                    "item_code": item_code,
                    "item_name": item.get("item_name", item_code),
                    "item_group": item_group,
                    "stock_uom": "Nos",
                    "is_stock_item": 1
                }).insert(ignore_permissions=True)
                print(f"Created Item: {item_code}")
            else:
                print(f"Item already exists: {item_code}")
                
        frappe.db.commit()
        print("Done!")
    else:
        print(f"Failed to fetch: {response.status_code} {response.text}")

