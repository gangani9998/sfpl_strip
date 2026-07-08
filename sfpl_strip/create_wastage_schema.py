import frappe

def create_wastage_schema():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # 1. Create Child Table DocType
    if not frappe.db.exists("DocType", "Strip Wastage Entry"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Strip Wastage Entry",
            "module": "SFPL Strip",
            "custom": 1,
            "istable": 1,
            "editable_grid": 1,
            "fields": [
                {
                    "fieldname": "reason",
                    "fieldtype": "Select",
                    "label": "Reason",
                    "options": "Startup\nBreakdown\nMaterial Shortage\nPower Cut\nOther",
                    "in_list_view": 1,
                    "reqd": 1
                },
                {
                    "fieldname": "wastage_qty",
                    "fieldtype": "Float",
                    "label": "Wastage Qty (kg)",
                    "in_list_view": 1,
                    "reqd": 1
                }
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created Strip Wastage Entry child table.")
    else:
        print("Strip Wastage Entry already exists.")

    # 2. Add to Strip Work Schedule
    ws = frappe.get_doc("DocType", "Strip Work Schedule")
    modified = False
    
    if not any(f.fieldname == "wastage_entries" for f in ws.fields):
        ws.append("fields", {
            "fieldname": "wastage_entries",
            "fieldtype": "Table",
            "options": "Strip Wastage Entry",
            "label": "Wastage Log",
            "insert_after": "wastage_qty"
        })
        modified = True
        
    if not any(f.fieldname == "wastage_posted" for f in ws.fields):
        ws.append("fields", {
            "fieldname": "wastage_posted",
            "fieldtype": "Check",
            "label": "Wastage Posted",
            "hidden": 1,
            "default": "0"
        })
        modified = True
        
    if modified:
        # We also want to hide or make read_only the old wastage_qty since now it's calculated from the table.
        # Let's set the old wastage_qty to read_only
        for f in ws.fields:
            if f.fieldname == "wastage_qty":
                f.read_only = 1
                
        # sort fields
        wastage_idx = 0
        for f in ws.fields:
            if f.fieldname == "wastage_qty":
                wastage_idx = f.idx
                break
                
        for f in ws.fields:
            if f.fieldname == "wastage_entries":
                f.idx = wastage_idx + 0.5
                break
                
        ws.fields.sort(key=lambda x: getattr(x, 'idx', 999))
        for i, f in enumerate(ws.fields):
            f.idx = i + 1
            
        ws.save(ignore_permissions=True)
        print("Added wastage_entries and wastage_posted to Strip Work Schedule.")
        
    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    create_wastage_schema()
