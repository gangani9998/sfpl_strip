import frappe

def add_production_analysis_tab():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    # Check if tab already exists
    has_tab = any(f.fieldname == "production_analysis_tab" for f in doc.fields)
    
    if not has_tab:
        # We'll append the fields at the end of the form
        fields_to_add = [
            {
                "fieldname": "production_analysis_tab",
                "fieldtype": "Tab Break",
                "label": "Production Analysis"
            },
            {
                "fieldname": "batch_production_meter",
                "fieldtype": "Float",
                "label": "Batch Production - Meter",
                "read_only": 1
            },
            {
                "fieldname": "submitted_production_meter",
                "fieldtype": "Float",
                "label": "Submitted Production - Meter",
                "read_only": 1
            },
            {
                "fieldname": "draft_production_meter",
                "fieldtype": "Float",
                "label": "Draft Production - Meter",
                "read_only": 1
            },
            {
                "fieldname": "col_break_pa1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "total_produced_meter",
                "fieldtype": "Float",
                "label": "Total Produced - Meter",
                "read_only": 1
            },
            {
                "fieldname": "remain_production_meter",
                "fieldtype": "Float",
                "label": "Remain Production - Meter",
                "read_only": 1
            },
            {
                "fieldname": "total_roll",
                "fieldtype": "Int",
                "label": "Total Roll",
                "read_only": 1
            },
            {
                "fieldname": "col_break_pa2",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "average_gsm",
                "fieldtype": "Float",
                "label": "Average GSM",
                "read_only": 1
            },
            {
                "fieldname": "yarn_coating_ratio",
                "fieldtype": "Data",
                "label": "Yarn Coating Ratio",
                "read_only": 1
            }
        ]
        
        for field in fields_to_add:
            doc.append("fields", field)
            
        # Frappe automatically handles sorting appended items to the end.
        for i, f in enumerate(doc.fields):
            f.idx = i + 1
            
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("Added Production Analysis tab and fields to Work Schedule.")
    else:
        print("Production Analysis tab already exists.")
        
    frappe.destroy()

if __name__ == "__main__":
    add_production_analysis_tab()
