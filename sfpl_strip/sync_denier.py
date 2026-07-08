import frappe
import requests

def sync_denier():
    frappe.init(site="site1.localhost")
    frappe.connect()

    url = 'https://erp.shivoham.tech/api/resource/Item?limit_page_length=0&fields=["name","denier"]'
    headers = {
        'Authorization': 'token 54cd3cba3400d6d:beb13b452346ce7'
    }

    try:
        print("Fetching denier values from live ERP...")
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch: {response.text}")
            return
            
        items = response.json().get('data', [])
        count = 0
        for item in items:
            name = item.get("name")
            denier = item.get("denier")
            if denier is not None:
                if frappe.db.exists("Item", name):
                    frappe.db.set_value("Item", name, "denier", denier)
                    count += 1
                    
        frappe.db.commit()
        print(f"Successfully updated denier for {count} items.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        frappe.destroy()

if __name__ == "__main__":
    sync_denier()
