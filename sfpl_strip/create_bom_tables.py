import frappe

def create_child_tables():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # Create Strip Production Coating
    if not frappe.db.exists("DocType", "Strip Production Coating"):
        coating_doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Strip Production Coating",
            "module": "SFPL Strip",
            "custom": 0,
            "istable": 1,
            "fields": [
                {
                    "fieldname": "coating_material",
                    "fieldtype": "Link",
                    "label": "Coating Material",
                    "options": "Item",
                    "read_only": 1,
                    "in_list_view": 1
                },
                {
                    "fieldname": "ratio",
                    "fieldtype": "Float",
                    "label": "Ratio (%)",
                    "read_only": 1,
                    "in_list_view": 1
                },
                {
                    "fieldname": "weight",
                    "fieldtype": "Float",
                    "label": "Weight (kg)",
                    "read_only": 1,
                    "in_list_view": 1
                }
            ]
        })
        coating_doc.insert(ignore_permissions=True)
        print("Created Strip Production Coating.")

    # Create Strip Production Yarn
    if not frappe.db.exists("DocType", "Strip Production Yarn"):
        yarn_doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Strip Production Yarn",
            "module": "SFPL Strip",
            "custom": 0,
            "istable": 1,
            "fields": [
                {
                    "fieldname": "yarn",
                    "fieldtype": "Link",
                    "label": "Yarn",
                    "options": "Item",
                    "read_only": 1,
                    "in_list_view": 1
                },
                {
                    "fieldname": "denier",
                    "fieldtype": "Float",
                    "label": "Denier",
                    "read_only": 1,
                    "in_list_view": 1
                },
                {
                    "fieldname": "number_of_yarn",
                    "fieldtype": "Int",
                    "label": "No. of Yarn",
                    "read_only": 1,
                    "in_list_view": 1
                },
                {
                    "fieldname": "denier_strength",
                    "fieldtype": "Float",
                    "label": "Denier Strength",
                    "read_only": 1,
                    "in_list_view": 0
                },
                {
                    "fieldname": "weight",
                    "fieldtype": "Float",
                    "label": "Weight (kg)",
                    "read_only": 1,
                    "in_list_view": 1
                }
            ]
        })
        yarn_doc.insert(ignore_permissions=True)
        print("Created Strip Production Yarn.")

    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    create_child_tables()
