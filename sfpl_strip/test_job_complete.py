import frappe

def run():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # Get the specific document
    doc = frappe.get_doc("Strip Work Schedule", "SWS-2026-00009")
    
    # Try to transition to Job Complete
    print(f"Current State: {doc.workflow_state}")
    
    # Normally workflow does this:
    doc.workflow_state = "Job Complete"
    
    try:
        doc.save(ignore_permissions=True)
        print("Successfully transitioned!")
    except Exception as e:
        print(f"Error saving: {e}")
        
    frappe.destroy()

if __name__ == "__main__":
    run()
