import frappe

def get_strip_work_schedule(arg):
    session_user_roles = frappe.get_roles(frappe.session.user)
    if frappe.session.user != "Administrator" and (
        "Operator Only" in session_user_roles and "System Manager" not in session_user_roles
    ):
        return "(`tabStrip Work Schedule`.workflow_state IN ('Under Production', 'Under production'))"

def get_strip_item(arg):
    session_user_roles = frappe.get_roles(frappe.session.user)
    if frappe.session.user != "Administrator" and (
        "Operator Only" in session_user_roles and "System Manager" not in session_user_roles
    ):
        return "(`tabItem`.is_quality_item = 1)"
