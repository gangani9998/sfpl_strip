from frappe import _

def get_data():
    return {
        "fieldname": "strip_work_schedule",
        "transactions": [
            {
                "label": _("Production"),
                "items": ["Strip Production Entry"]
            }
        ]
    }
