import frappe
import requests

def sync_items():
    frappe.init(site="site1.localhost")
    frappe.connect()

    url = 'https://erp.shivoham.tech/api/resource/Item?limit_page_length=0&fields=["*"]'
    headers = {
        'Authorization': 'token 54cd3cba3400d6d:beb13b452346ce7'
    }

    try:
        print("Fetching items from live ERP...")
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch items: {response.text}")
            return
            
        items = response.json().get('data', [])
        print(f"Found {len(items)} items. Syncing to local...")
        
        success = 0
        
        for idx, item_data in enumerate(items):
            item_code = item_data.get('item_code')
            
            # Ensure Item Group exists
            item_group = item_data.get("item_group")
            if item_group and not frappe.db.exists("Item Group", item_group):
                frappe.get_doc({
                    "doctype": "Item Group",
                    "item_group_name": item_group,
                    "parent_item_group": "All Item Groups",
                    "is_group": 0
                }).insert(ignore_permissions=True, ignore_links=True, ignore_mandatory=True)

            # Ensure UOM exists
            stock_uom = item_data.get("stock_uom")
            if stock_uom and not frappe.db.exists("UOM", stock_uom):
                frappe.get_doc({
                    "doctype": "UOM",
                    "uom_name": stock_uom
                }).insert(ignore_permissions=True, ignore_links=True, ignore_mandatory=True)
                
            # Clean up read-only / system fields
            for field in ["name", "creation", "modified", "modified_by", "owner", "_user_tags", "_comments", "_assign", "_liked_by"]:
                item_data.pop(field, None)
                
            if frappe.db.exists("Item", item_code):
                # Update existing
                doc = frappe.get_doc("Item", item_code)
                doc.update(item_data)
                doc.save(ignore_permissions=True, ignore_links=True, ignore_mandatory=True)
            else:
                # Insert new
                doc = frappe.get_doc({"doctype": "Item"})
                doc.update(item_data)
                doc.insert(ignore_permissions=True, ignore_links=True, ignore_mandatory=True)
                
            success += 1
            if success % 20 == 0:
                print(f"Synced {success}/{len(items)}...")

        frappe.db.commit()
        print(f"Successfully synced {success} items to local DB.")

    except Exception as e:
        print(f"Error during sync: {e}")
    finally:
        frappe.destroy()

if __name__ == "__main__":
    sync_items()
