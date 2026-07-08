import frappe

def create_workflow():
    frappe.init(site="site1.localhost")
    frappe.connect()

    try:
        states = ["Draft", "Pending", "Approved", "Waiting", "Drawing", "Under Production", "Job Complete"]
        for s in states:
            if not frappe.db.exists("Workflow State", s):
                doc = frappe.get_doc({
                    "doctype": "Workflow State",
                    "workflow_state_name": s
                })
                # map doc status: Job Complete and Under Production can be 1 (Submitted), Draft is 0
                if s in ["Under Production", "Job Complete"]:
                    doc.doc_status = 1
                else:
                    doc.doc_status = 0
                doc.insert(ignore_permissions=True)

        actions = ["Submit for Review", "Approve", "Wait", "Start Drawing", "Start Production", "Complete Job"]
        for a in actions:
            if not frappe.db.exists("Workflow Action Master", a):
                doc = frappe.get_doc({
                    "doctype": "Workflow Action Master",
                    "workflow_action_name": a
                })
                doc.insert(ignore_permissions=True)

        if not frappe.db.exists("Workflow", "Strip Work Schedule Workflow"):
            doc = frappe.get_doc({
                "doctype": "Workflow",
                "workflow_name": "Strip Work Schedule Workflow",
                "document_type": "Strip Work Schedule",
                "is_active": 1,
                "workflow_state_field": "production_status",
                "states": [
                    {"state": "Draft", "doc_status": 0, "allow_edit": "System Manager"},
                    {"state": "Pending", "doc_status": 0, "allow_edit": "System Manager"},
                    {"state": "Approved", "doc_status": 0, "allow_edit": "System Manager"},
                    {"state": "Waiting", "doc_status": 0, "allow_edit": "System Manager"},
                    {"state": "Drawing", "doc_status": 0, "allow_edit": "System Manager"},
                    {"state": "Under Production", "doc_status": 1, "allow_edit": "System Manager"},
                    {"state": "Job Complete", "doc_status": 1, "allow_edit": "System Manager"}
                ],
                "transitions": [
                    {"state": "Draft", "action": "Submit for Review", "next_state": "Pending", "allowed": "System Manager"},
                    {"state": "Pending", "action": "Approve", "next_state": "Approved", "allowed": "System Manager"},
                    {"state": "Approved", "action": "Wait", "next_state": "Waiting", "allowed": "System Manager"},
                    {"state": "Approved", "action": "Start Drawing", "next_state": "Drawing", "allowed": "System Manager"},
                    {"state": "Waiting", "action": "Start Drawing", "next_state": "Drawing", "allowed": "System Manager"},
                    {"state": "Drawing", "action": "Start Production", "next_state": "Under Production", "allowed": "System Manager"},
                    {"state": "Under Production", "action": "Complete Job", "next_state": "Job Complete", "allowed": "System Manager"}
                ]
            })
            doc.insert(ignore_permissions=True)
            print("Workflow created.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        frappe.db.commit()
        frappe.destroy()

if __name__ == "__main__":
    create_workflow()
