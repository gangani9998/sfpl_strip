import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create():
    if not frappe.db.exists("DocType", "Strip System Strength Data"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Strip System Strength Data",
            "module": "SFPL Strip",
            "custom": 0,
            "istable": 1,
            "fields": [
                {
                    "fieldname": "specimen_no",
                    "fieldtype": "Data",
                    "label": "Specimen No",
                    "in_list_view": 1
                },
                {
                    "fieldname": "system_strength",
                    "fieldtype": "Float",
                    "label": "System Strength",
                    "in_list_view": 1
                },
                {
                    "fieldname": "tensile_strength",
                    "fieldtype": "Float",
                    "label": "Tensile Strength",
                    "in_list_view": 1
                }
            ]
        })
        doc.insert()
        print("Created Strip System Strength Data Child Table")

    # For MTC Strip we just add fields to its existing JSON by modifying the DocType
    mtc = frappe.get_doc("DocType", "MTC Strip")
    
    # Check if system_strength_data field exists
    if not any(f.fieldname == "system_strength_data" for f in mtc.fields):
        mtc.append("fields", {
            "fieldname": "system_strength_data",
            "fieldtype": "Table",
            "label": "System Strength Test Data",
            "options": "Strip System Strength Data",
            "insert_after": "specimen_data"
        })
        
    if not any(f.fieldname == "mean_system_strength" for f in mtc.fields):
        mtc.append("fields", {
            "fieldname": "mean_system_strength",
            "fieldtype": "Float",
            "label": "Mean System Strength",
            "insert_after": "mean_elongation_ultimate",
            "read_only": 1
        })
        
    mtc.save()
    print("Added custom fields to MTC Strip DocType")
    
    frappe.db.commit()
