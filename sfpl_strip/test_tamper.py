import frappe

def test_tamper_wastage():
    frappe.init(site="site1.localhost")
    frappe.connect()

    try:
        doc = frappe.get_doc("Strip Work Schedule", "SWS-2026-00007")
        
        # Tamper: add a new row
        doc.append("wastage_entries", {
            "reason": "Startup",
            "wastage_qty": 500
        })
        
        print("Attempting to save tampered document...")
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print("FAIL: Document saved successfully despite tampering!")
    except Exception as e:
        print(f"SUCCESS: Tamper attempt rejected! Error: {e}")
        
    frappe.destroy()

if __name__ == "__main__":
    test_tamper_wastage()
