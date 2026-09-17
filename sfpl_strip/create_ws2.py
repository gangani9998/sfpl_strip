import frappe

def create():
    lines = frappe.get_all("Extrusion Line")
    line = lines[0].name if lines else None
    
    dies = frappe.get_all("Die")
    die = dies[0].name if dies else None
    
    sizers = frappe.get_all("Sizer")
    sizer = sizers[0].name if sizers else None
    
    if not line or not die or not sizer:
        print("Missing Extrusion Line, Die or Sizer in DB. Please create one manually in UI first.")
        return
        
    wastage_item = "TEST-WASTAGE"
    if not frappe.db.exists("Item", wastage_item):
        frappe.get_doc({
            "doctype": "Item",
            "item_code": wastage_item,
            "item_name": "Test Wastage",
            "item_group": "Products",
            "stock_uom": "Kg",
            "is_stock_item": 1
        }).insert(ignore_permissions=True)
        
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
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"Created Strip Work Schedule: {doc.name}")

