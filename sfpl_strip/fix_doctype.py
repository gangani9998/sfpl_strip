import frappe

def fix_doctype():
    frappe.init(site="site1.localhost")
    frappe.connect()

    # Get the DocType document
    doc = frappe.get_doc("DocType", "Strip Work Schedule")
    
    # Track seen fieldnames
    seen = set()
    unique_fields = []
    
    for f in doc.fields:
        if f.fieldname not in seen:
            seen.add(f.fieldname)
            unique_fields.append(f)
            
    # Keep only unique fields
    doc.fields = unique_fields
    
    # Remove 'created_by'
    doc.fields = [f for f in doc.fields if f.fieldname != 'created_by']
    
    # Move 'created_on' above 'die_no'
    created_on_idx = -1
    die_no_idx = -1
    
    for i, f in enumerate(doc.fields):
        if f.fieldname == 'created_on':
            created_on_idx = i
        if f.fieldname == 'die_no':
            die_no_idx = i
            
    if created_on_idx != -1 and die_no_idx != -1:
        # Remove created_on from current position
        created_on_field = doc.fields.pop(created_on_idx)
        
        # Find new index for die_no since the list shifted
        for i, f in enumerate(doc.fields):
            if f.fieldname == 'die_no':
                die_no_idx = i
                break
                
        # Insert created_on before die_no
        doc.fields.insert(die_no_idx, created_on_field)
        
    # Re-sequence idx
    for i, f in enumerate(doc.fields):
        f.idx = i + 1
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Fixed Strip Work Schedule JSON and DB!")

if __name__ == "__main__":
    fix_doctype()
