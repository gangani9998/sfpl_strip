import frappe

def test_new_logic():
    frappe.init(site="site1.localhost")
    frappe.connect()

    try:
        # Test 1: Cancellation Escape Hatch
        ws = frappe.new_doc("Strip Work Schedule")
        ws.extrusion_line = frappe.get_all("Extrusion Line")[0].name
        ws.target_qty = 1000
        ws.roll_size = 100
        ws.target_gsm = 150
        ws.quality = frappe.get_all("Item", filters={"is_quality_item": 1})[0].name
        ws.die_no = "Test Die"
        ws.sizer_no = "Test Sizer"
        ws.wastage_item = frappe.get_all("Item", filters={"item_group": "Scrap"})[0].name
        ws.insert(ignore_permissions=True)
        
        # Change state to Under Production
        ws.workflow_state = "Under Production"
        ws.save(ignore_permissions=True)
        
        # Try to cancel
        print("Testing cancellation from Under Production...")
        ws.cancel()
        print("SUCCESS: Cancellation Escape Hatch works!")
        
        # Test 2: Theoretical Wastage Engine
        ws2 = frappe.new_doc("Strip Work Schedule")
        ws2.extrusion_line = frappe.get_all("Extrusion Line")[0].name
        ws2.target_qty = 1000
        ws2.roll_size = 100
        ws2.target_gsm = 150
        ws2.quality = frappe.get_all("Item", filters={"is_quality_item": 1})[0].name
        ws2.die_no = "Test Die 2"
        ws2.sizer_no = "Test Sizer 2"
        ws2.wastage_item = frappe.get_all("Item", filters={"item_group": "Scrap"})[0].name
        
        # Add warp data and coating ratios for math
        ws2.append("warp_data", {
            "yarn": frappe.get_all("Item", filters={"item_group": "Yarn"})[0].name,
            "denier": 6000,
            "number_of_yarn": 110,
            "denier_strength": 6
        })
        
        ws2.append("default_coating_ratios", {
            "coating_material": frappe.get_all("Item", filters={"item_group": "Raw Material"})[0].name,
            "ratio": 100
        })
        
        ws2.insert(ignore_permissions=True)
        
        # Add 10kg wastage
        ws2.append("wastage_entries", {
            "reason": "Startup",
            "wastage_qty": 10
        })
        ws2.workflow_state = "Under Production"
        ws2.save(ignore_permissions=True)
        
        # Change state to Job Complete
        print("Testing Theoretical Wastage Engine...")
        ws2.workflow_state = "Job Complete"
        ws2.save(ignore_permissions=True)
        
        if ws2.wastage_posted == 1:
            print("SUCCESS: Wastage posted theoretically with 0 production entries!")
        else:
            print("FAIL: Wastage was not posted.")
            
        # Clean up
        ws2.cancel()
        
    except Exception as e:
        print(f"TEST FAILED: {e}")
        
    frappe.db.rollback() # Don't leave test data
    frappe.destroy()

if __name__ == "__main__":
    test_new_logic()
