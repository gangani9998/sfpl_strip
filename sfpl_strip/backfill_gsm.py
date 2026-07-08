import frappe
from frappe.utils import flt

def backfill_gsm():
    frappe.init(site="site1.localhost")
    frappe.connect()

    entries = frappe.get_all("Strip Production Entry", fields=["name", "roll_net_weight", "roll_length", "strip_work_schedule"])
    
    schedules_to_update = set()
    
    for e in entries:
        net = flt(e.roll_net_weight)
        length = flt(e.roll_length)
        if length > 0:
            gsm = (net / length) * 1000
            frappe.db.set_value("Strip Production Entry", e.name, "gsm", gsm)
        
        if e.strip_work_schedule:
            schedules_to_update.add(e.strip_work_schedule)
            
    # Update work schedules
    for ws_name in schedules_to_update:
        ws = frappe.get_doc("Strip Work Schedule", ws_name)
        ws.update_production_analysis()
        ws.flags.ignore_validate = True
        ws.save(ignore_permissions=True)
        
    frappe.db.commit()
    print("Backfilled GSM for existing entries and updated schedules.")
    frappe.destroy()

if __name__ == "__main__":
    backfill_gsm()
