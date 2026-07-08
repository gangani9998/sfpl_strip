import frappe

def fix_schema():
    frappe.init(site="site1.localhost")
    frappe.connect()

    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    # Remove created_by
    doc.fields = [f for f in doc.fields if f.fieldname != "created_by"]
    
    # Ensure created_on exists and place it above die_no
    created_on_field = None
    for f in doc.fields:
        if f.fieldname == "created_on":
            created_on_field = f
            break
            
    if not created_on_field:
        created_on_field = frappe.new_doc("DocField")
        created_on_field.fieldname = "created_on"
        created_on_field.fieldtype = "Datetime"
        created_on_field.label = "Created On"
        created_on_field.read_only = 1
        created_on_field.insert(ignore_permissions=True)
    
    # Rebuild fields list to place created_on right before die_no
    new_fields = []
    inserted = False
    
    # First remove created_on from its current place
    doc.fields = [f for f in doc.fields if f.fieldname != "created_on"]
    
    for f in doc.fields:
        if f.fieldname == "die_no" and not inserted:
            # Place created_on right before die_no
            # Wait, die_no is in column 2. Extrusion Line is in column 1.
            # If we want it "above die no", it should be in the same column break as die_no.
            # But the user just said "above the die no".
            
            # Let's create the field properly as a dict
            new_fields.append({
                "fieldname": "created_on",
                "fieldtype": "Datetime",
                "label": "Created On",
                "read_only": 1
            })
            inserted = True
            
        new_fields.append(f.as_dict())
        
    doc.fields = []
    for nf in new_fields:
        doc.append("fields", nf)
        
    doc.save()
    frappe.db.commit()
    
    # Export fixtures/customizations if needed, or just let Frappe handle it via developer mode
    
    print("Schema updated successfully!")

if __name__ == "__main__":
    fix_schema()
