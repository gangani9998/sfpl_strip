import frappe

def create():
    # Setup dependencies
    if not frappe.db.exists("Extrusion Line", "Line-1"):
        frappe.get_doc({"doctype": "Extrusion Line", "extrusion_line": "Line-1"}).insert(ignore_permissions=True)
    if not frappe.db.exists("Die", "Die-1"):
        frappe.get_doc({"doctype": "Die", "die_number": "Die-1"}).insert(ignore_permissions=True)
    if not frappe.db.exists("Sizer", "Sizer-1"):
        frappe.get_doc({"doctype": "Sizer", "sizer_number": "Sizer-1"}).insert(ignore_permissions=True)
    
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
        
    # Cancel or complete any active job on Line-1 so we can create a new one
    active = frappe.db.get_value("Strip Work Schedule", {"extrusion_line": "Line-1", "docstatus": ["<", 2], "workflow_state": ["in", ["Drawing", "Under Production", "Under production"]]}, "name")
    if active:
        frappe.db.set_value("Strip Work Schedule", active, "workflow_state", "Job Complete")
        
    doc = frappe.get_doc({
        "doctype": "Strip Work Schedule",
        "extrusion_line": "Line-1",
        "quality": "STO-ITEM-00113",
        "target_qty": 10000,
        "roll_size": 1000,
        "target_gsm": 45,
        "die_no": "Die-1",
        "sizer_no": "Sizer-1",
        "wastage_item": wastage_item,
        "standard_strip_width": 25.0,
        "default_coating_ratios": [
            {"coating_material": wastage_item, "ratio": 100} # Dummy
        ]
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"Created Strip Work Schedule: {doc.name}")

