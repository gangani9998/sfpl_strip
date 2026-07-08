import frappe

def add_reproduction_transition():
    frappe.init(site="site1.localhost")
    frappe.connect()

    wf = frappe.get_doc("Workflow", "Strip Work Schedule Workflow")
    
    has_reprod = any(t.state == "Job Complete" and t.next_state == "Under Production" for t in wf.transitions)
    
    if not has_reprod:
        wf.append("transitions", {
            "state": "Job Complete",
            "action": "Re-Production",
            "next_state": "Under Production",
            "allowed": "Manufacturing User",
            "allow_self_approval": 1
        })
        
        wf.append("transitions", {
            "state": "Job Complete",
            "action": "Re-Production",
            "next_state": "Under Production",
            "allowed": "System Manager",
            "allow_self_approval": 1
        })
        
        wf.save(ignore_permissions=True)
        frappe.db.commit()
        print("Added Re-Production transition to Workflow.")

    frappe.destroy()

if __name__ == "__main__":
    add_reproduction_transition()
