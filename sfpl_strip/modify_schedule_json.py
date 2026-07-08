import json
import sys

def modify_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    fields = data.get('fields', [])
    
    # 1. Remove 'created_by'
    fields = [f for f in fields if f.get('fieldname') != 'created_by']
    
    # 2. Extract 'created_on'
    created_on_field = None
    for f in fields:
        if f.get('fieldname') == 'created_on':
            created_on_field = f
            break
            
    if created_on_field:
        fields.remove(created_on_field)
        
        # 3. Find index of 'die_no'
        die_no_idx = -1
        for i, f in enumerate(fields):
            if f.get('fieldname') == 'die_no':
                die_no_idx = i
                break
                
        if die_no_idx != -1:
            fields.insert(die_no_idx, created_on_field)
        else:
            fields.append(created_on_field)
            
    data['fields'] = fields
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=1)
        f.write("\n")
        
    print("Modified JSON successfully.")

if __name__ == "__main__":
    modify_json(sys.argv[1])
