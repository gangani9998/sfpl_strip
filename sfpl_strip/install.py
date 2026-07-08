from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    create_custom_fields(CUSTOM_FIELDS, ignore_validate=False)

CUSTOM_FIELDS = {
    "Batch": [
        {
            "fieldname": "strip_work_schedule",
            "fieldtype": "Data",
            "insert_after": "expiry_date",
            "label": "Strip Work Schedule (Lot No)",
            "read_only": 1
        },
        {
            "fieldname": "strip_production_entry",
            "fieldtype": "Data",
            "insert_after": "strip_work_schedule",
            "label": "Strip Production Entry (Roll No)",
            "read_only": 1
        }
    ],
    "Stock Entry": [
        {
            "fieldname": "strip_production_entry",
            "fieldtype": "Link",
            "insert_after": "stock_entry_type",
            "label": "Strip Production Entry (Roll No)",
            "options": "Strip Production Entry",
            "read_only": 1
        }
    ]
}
