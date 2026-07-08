import frappe
import json

def update_doctypes():
    frappe.init(site="site1.localhost")
    frappe.connect()

    try:
        # Create Strip Coating Ratio (Child Table)
        if not frappe.db.exists("DocType", "Strip Coating Ratio"):
            doc = frappe.get_doc({
                "doctype": "DocType",
                "name": "Strip Coating Ratio",
                "module": "SFPL Strip",
                "custom": 0,
                "istable": 1,
                "editable_grid": 1,
                "fields": [
                    {
                        "fieldname": "coating_material",
                        "fieldtype": "Link",
                        "options": "Item",
                        "label": "Coating Material",
                        "in_list_view": 1,
                        "reqd": 1
                    },
                    {
                        "fieldname": "ratio",
                        "fieldtype": "Float",
                        "label": "Ratio (%)",
                        "in_list_view": 1,
                        "reqd": 1
                    }
                ]
            })
            doc.insert(ignore_permissions=True)
            print("Strip Coating Ratio doctype created.")
        
        # Update Strip Work Schedule fields
        sws = frappe.get_doc("DocType", "Strip Work Schedule")
        
        sws.fields = []
        fields = [
            # Settings / Setup Section (Perm Level 1)
            {"fieldname": "setup_section", "fieldtype": "Section Break", "label": "Default Settings (Manager Only)", "permlevel": 1},
            {"fieldname": "default_yarn_item", "fieldtype": "Link", "options": "Item", "label": "Default Yarn Item", "permlevel": 1},
            {"fieldname": "default_paper_tube", "fieldtype": "Link", "options": "Item", "label": "Default Paper Tube", "permlevel": 1},
            {"fieldname": "column_break_setup", "fieldtype": "Column Break", "permlevel": 1},
            {"fieldname": "default_coating_ratios", "fieldtype": "Table", "options": "Strip Coating Ratio", "label": "Default Coating Ratios", "permlevel": 1},
            
            # Core Schedule Section
            {"fieldname": "schedule_section", "fieldtype": "Section Break", "label": "Work Schedule"},
            {"fieldname": "extrusion_line", "fieldtype": "Link", "options": "Extrusion Line", "label": "Extrusion Line", "reqd": 1},
            {"fieldname": "quality", "fieldtype": "Link", "options": "Item", "label": "Quality (Item)", "reqd": 1},
            {"fieldname": "column_break_schedule", "fieldtype": "Column Break"},
            {"fieldname": "production_status", "fieldtype": "Select", "label": "Production Status", "options": "\nDraft\nPending\nApproved\nWaiting\nDrawing\nUnder Production\nJob Complete", "default": "Draft", "reqd": 1, "in_list_view": 1},
            
            # Analytics Tab
            {"fieldname": "analytics_tab", "fieldtype": "Tab Break", "label": "Analytics"},
            {"fieldname": "total_production", "fieldtype": "Float", "label": "Total Production", "read_only": 1},
            {"fieldname": "total_roll_count", "fieldtype": "Int", "label": "Total Roll Count", "read_only": 1},
            
            # Wastage Section (Appears at Job Complete)
            {"fieldname": "wastage_section", "fieldtype": "Section Break", "label": "End of Production (Wastage)", "depends_on": "eval:doc.production_status=='Job Complete'"},
            {"fieldname": "wastage_item", "fieldtype": "Link", "options": "Item", "label": "Wastage/Scrap Item", "mandatory_depends_on": "eval:doc.production_status=='Job Complete'"},
            {"fieldname": "wastage_qty", "fieldtype": "Float", "label": "Wastage Qty (kg)", "mandatory_depends_on": "eval:doc.production_status=='Job Complete'"}
        ]
        
        for f in fields:
            sws.append("fields", f)
            
        sws.save(ignore_permissions=True)
        print("Strip Work Schedule updated.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        frappe.db.commit()
        frappe.destroy()

if __name__ == "__main__":
    update_doctypes()
