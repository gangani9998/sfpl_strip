import frappe

def run():
    with open("/Users/jaykumargangani/frappe-bench-v16/current_html.txt", "r") as f:
        lines = f.readlines()
        html_content = "".join(lines[1:]).strip()
    
    pf = frappe.get_doc("Print Format", "Packing List Copy")
    pf.html = html_content
    pf.save()
    frappe.db.commit()
    print("Packing List HTML updated successfully.")
