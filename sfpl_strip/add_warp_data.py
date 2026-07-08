import frappe

def add_warp_data():
    frappe.init(site="site1.localhost")
    frappe.connect()

    try:
        # Create Strip Yarn Data (Child Table)
        if not frappe.db.exists("DocType", "Strip Yarn Data"):
            doc = frappe.get_doc({
                "doctype": "DocType",
                "name": "Strip Yarn Data",
                "module": "SFPL Strip",
                "custom": 0,
                "istable": 1,
                "editable_grid": 1,
                "fields": [
                    {
                        "fieldname": "yarn",
                        "fieldtype": "Link",
                        "options": "Item",
                        "label": "Yarn",
                        "in_list_view": 1,
                        "reqd": 1
                    },
                    {
                        "fieldname": "denier",
                        "fieldtype": "Float",
                        "label": "Denier",
                        "fetch_from": "yarn.denier",
                        "in_list_view": 1,
                        "read_only": 1
                    },
                    {
                        "fieldname": "number_of_yarn",
                        "fieldtype": "Int",
                        "label": "Number of Yarn",
                        "in_list_view": 1,
                        "reqd": 1
                    },
                    {
                        "fieldname": "denier_strength",
                        "fieldtype": "Float",
                        "label": "Denier Strength",
                        "in_list_view": 1,
                        "precision": "6"
                    }
                ]
            })
            doc.insert(ignore_permissions=True)
            print("Strip Yarn Data child table created.")

        # Update Strip Work Schedule
        sws = frappe.get_doc("DocType", "Strip Work Schedule")
        
        # Check if warp_data is already there
        if not any(f.fieldname == "warp_data" for f in sws.fields):
            # Insert warp_data before column_break_setup or at a specific location
            new_field = {
                "fieldname": "warp_data",
                "fieldtype": "Table",
                "options": "Strip Yarn Data",
                "label": "Warp Data",
                "insert_after": "default_yarn_item",
                "permlevel": 1
            }
            sws.append("fields", new_field)
            sws.save(ignore_permissions=True)
            print("Added warp_data table to Strip Work Schedule.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        frappe.db.commit()
        frappe.destroy()

if __name__ == "__main__":
    add_warp_data()
