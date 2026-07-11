from frappe import _

def get_data():
    return {
        "fieldname": "strip_work_schedule",
        "non_standard_fieldnames": {
            "MTC Strip": "lot_no"
        },
        "transactions": [
            {
                "label": _("Connections"),
                "items": ["Strip Production Entry", "MTC Strip"]
            }
        ]
    }
