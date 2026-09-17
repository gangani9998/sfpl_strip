import frappe

def create():
    lines = frappe.get_all("Extrusion Line")
    line = lines[0].name
    dies = frappe.get_all("Die")
    die = dies[0].name
    sizers = frappe.get_all("Sizer")
    sizer = sizers[0].name
    
    wastage_item = "TEST-WASTAGE"
        
    doc = frappe.get_doc({
        "doctype": "Strip Work Schedule",
        "extrusion_line": line,
        "quality": "STO-ITEM-00113",
        "target_qty": 10000,
        "roll_size": 1000,
        "target_gsm": 45,
        "die_no": die,
        "sizer_no": sizer,
        "wastage_item": wastage_item,
        "standard_strip_width": 25.0,
        "default_coating_ratios": [
            {"coating_material": wastage_item, "ratio": 100}
        ],
        "warp_data": [
            {
                "yarn": "STO-ITEM-00037",
                "denier": 1000,
                "number_of_yarn": 10,
                "denier_strength": 7.5
            }
        ]
    })
    doc.insert(ignore_permissions=True)
    doc.submit()
    frappe.db.commit()
    print(f"Created NEW Strip Work Schedule: {doc.name}")

