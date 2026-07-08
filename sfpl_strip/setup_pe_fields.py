import frappe

def update_production_entry():
    frappe.init(site="site1.localhost")
    frappe.connect()

    try:
        pe = frappe.get_doc("DocType", "Strip Production Entry")
        
        # We need autoname by naming_series field
        pe.autoname = "naming_series:"
        pe.is_submittable = 1
        pe.fields = []
        
        fields = [
            {"fieldname": "naming_series", "fieldtype": "Select", "label": "Naming Series", "options": "G-PE-.YYYY.-.#####\nP-PE-.YYYY.-.#####", "reqd": 1},
            {"fieldname": "strip_work_schedule", "fieldtype": "Link", "options": "Strip Work Schedule", "label": "Strip Work Schedule", "reqd": 1, "in_list_view": 1},
            {"fieldname": "posting_date", "fieldtype": "Date", "label": "Posting Date", "default": "Today", "reqd": 1},
            {"fieldname": "posting_time", "fieldtype": "Time", "label": "Posting Time", "default": "Now", "reqd": 1},
            {"fieldname": "strip_product_code", "fieldtype": "Link", "options": "Item", "label": "Product Code (Item)", "reqd": 1},
            
            {"fieldname": "col_break_1", "fieldtype": "Column Break"},
            {"fieldname": "qr_code", "fieldtype": "Attach Image", "label": "QR Code", "read_only": 1},
            {"fieldname": "batch_no", "fieldtype": "Data", "label": "Batch No (Generated)", "read_only": 1},
            
            {"fieldname": "dim_section", "fieldtype": "Section Break", "label": "Roll Dimensions"},
            {"fieldname": "roll_length", "fieldtype": "Float", "label": "Roll Length (m)", "reqd": 1},
            {"fieldname": "roll_gross_weight", "fieldtype": "Float", "label": "Roll Gross Weight (kg)", "reqd": 1},
            {"fieldname": "col_break_2", "fieldtype": "Column Break"},
            {"fieldname": "papertube_weight", "fieldtype": "Float", "label": "Paper Tube Weight (kg)", "reqd": 1},
            {"fieldname": "roll_net_weight", "fieldtype": "Float", "label": "Roll Net Weight (kg)", "read_only": 1},
            
            {"fieldname": "params_section", "fieldtype": "Section Break", "label": "Extrusion Parameters"},
            {"fieldname": "barrel_z1", "fieldtype": "Float", "label": "Barrel Zone 1 Temp"},
            {"fieldname": "barrel_z2", "fieldtype": "Float", "label": "Barrel Zone 2 Temp"},
            {"fieldname": "barrel_z3", "fieldtype": "Float", "label": "Barrel Zone 3 Temp"},
            {"fieldname": "barrel_z4", "fieldtype": "Float", "label": "Barrel Zone 4 Temp"},
            {"fieldname": "barrel_z5", "fieldtype": "Float", "label": "Barrel Zone 5 Temp"},
            {"fieldname": "col_break_3", "fieldtype": "Column Break"},
            {"fieldname": "die_z1", "fieldtype": "Float", "label": "Die Zone 1 Temp"},
            {"fieldname": "die_z2", "fieldtype": "Float", "label": "Die Zone 2 Temp"},
            {"fieldname": "extruder_rpm", "fieldtype": "Float", "label": "Extruder RPM"},
            {"fieldname": "haul_off_rpm", "fieldtype": "Float", "label": "Haul-Off RPM"},
            {"fieldname": "water_temp", "fieldtype": "Float", "label": "Water Temp"}
        ]
        
        for f in fields:
            pe.append("fields", f)
            
        pe.save(ignore_permissions=True)
        print("Strip Production Entry updated.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        frappe.db.commit()
        frappe.destroy()

if __name__ == "__main__":
    update_production_entry()
