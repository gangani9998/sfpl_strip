import frappe

def execute():
    ws = frappe.get_doc("Strip Work Schedule", "SWS-2026-00019")
    if not ws.warp_data:
        ws.append("warp_data", {
            "yarn": "STO-ITEM-00037", # Using one of the items we updated earlier
            "denier": 1000,
            "number_of_yarn": 10,
            "denier_strength": 7.5
        })
        ws.save(ignore_permissions=True)
        frappe.db.commit()
        print("Added yarn to Work Schedule!")
