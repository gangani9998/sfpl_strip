import frappe

def create_mtc():
    frappe.init(site="site1.localhost")
    frappe.connect()

    try:
        mtcs = ["GS MTC", "PS MTC"]
        for mtc in mtcs:
            if not frappe.db.exists("DocType", mtc):
                doc = frappe.get_doc({
                    "doctype": "DocType",
                    "name": mtc,
                    "module": "SFPL Strip",
                    "custom": 0,
                    "autoname": "naming_series:",
                    "is_submittable": 1,
                    "fields": [
                        {"fieldname": "naming_series", "fieldtype": "Select", "label": "Naming Series", "options": "MTC-.YYYY.-.#####", "reqd": 1},
                        {"fieldname": "lot_no", "fieldtype": "Link", "options": "Strip Work Schedule", "label": "Lot No (Work Schedule)", "reqd": 1},
                        {"fieldname": "roll_no", "fieldtype": "Link", "options": "Strip Production Entry", "label": "Roll No (Batch)", "reqd": 1},
                        {"fieldname": "posting_date", "fieldtype": "Date", "label": "Posting Date", "default": "Today", "reqd": 1},
                        {"fieldname": "col_break", "fieldtype": "Column Break"},
                        {"fieldname": "qc_inspector", "fieldtype": "Link", "options": "Employee", "label": "QC Inspector"}
                    ],
                    "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
                })
                doc.insert(ignore_permissions=True)
                print(f"{mtc} doctype created and exported.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        frappe.db.commit()
        frappe.destroy()

if __name__ == "__main__":
    create_mtc()
