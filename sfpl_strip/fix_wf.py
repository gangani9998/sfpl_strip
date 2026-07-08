import frappe

def fix_workflow_and_depends():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # 1. Update Workflow
    wf = frappe.get_doc("Workflow", "Strip Work Schedule Workflow")
    if wf.workflow_state_field == "production_status":
        wf.workflow_state_field = "workflow_state"
        wf.save(ignore_permissions=True)
        print("Updated Workflow state field.")

    # 2. Update depends_on in DocField
    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    changed = False
    for f in doc.fields:
        if f.depends_on and "doc.production_status" in f.depends_on:
            f.depends_on = f.depends_on.replace("doc.production_status", "doc.workflow_state")
            changed = True
        if f.mandatory_depends_on and "doc.production_status" in f.mandatory_depends_on:
            f.mandatory_depends_on = f.mandatory_depends_on.replace("doc.production_status", "doc.workflow_state")
            changed = True
    
    if changed:
        doc.save(ignore_permissions=True)
        print("Updated depends_on rules in Strip Work Schedule.")

    frappe.db.commit()
    frappe.destroy()

if __name__ == "__main__":
    fix_workflow_and_depends()
