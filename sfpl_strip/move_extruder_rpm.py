import frappe

def move_extruder_rpm():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Production Entry")
    
    # find params_section idx
    params_idx = 0
    for f in doc.fields:
        if f.fieldname == "params_section":
            params_idx = f.idx
            break
            
    # move extruder_rpm to right after params_section
    for f in doc.fields:
        if f.fieldname == "extruder_rpm":
            f.idx = params_idx + 0.5
            break
            
    doc.fields.sort(key=lambda x: x.idx)
    
    # reassign integer idx
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Moved Extruder RPM to top left of Extrusion Parameters section.")
    frappe.destroy()

if __name__ == "__main__":
    move_extruder_rpm()
