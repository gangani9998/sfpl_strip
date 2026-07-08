import json
import os

filepath = "/Users/jaykumargangani/frappe-bench-v16/apps/sfpl_strip/sfpl_strip/sfpl_strip/doctype/strip_work_schedule/strip_work_schedule.json"

with open(filepath, 'r') as f:
    data = json.load(f)

unique_fields = []
seen = set()

for field in data['fields']:
    if field['fieldname'] not in seen:
        seen.add(field['fieldname'])
        unique_fields.append(field)

print(f"Original fields: {len(data['fields'])}")
print(f"Unique fields: {len(unique_fields)}")

data['fields'] = unique_fields

with open(filepath, 'w') as f:
    json.dump(data, f, indent=1)

print("Duplicates removed from JSON.")
