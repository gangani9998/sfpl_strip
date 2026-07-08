// Copyright (c) 2026, Jay Kumar Gangani and contributors
// For license information, please see license.txt

frappe.ui.form.on("Strip Work Schedule", {
    refresh(frm) {
        if (!frm.doc.created_on) {
            frm.set_value('created_on', frm.doc.creation || frappe.datetime.now_datetime());
        }


        // Filter Quality field to only show Items marked as Quality Item
        frm.set_query("quality", function () {
            return {
                filters: {
                    is_quality_item: 1
                }
            };
        });

        frm.set_query("default_paper_tube", function () {
            return {
                filters: {
                    item_group: "Packing Material"
                }
            };
        });

        frm.set_query("wastage_item", function () {
            return {
                filters: {
                    is_stock_item: 1
                }
            };
        });
        
        // Hide wastage section entirely if the schedule is in Draft (Drawing) state
        if (frm.doc.docstatus === 0) {
            frm.set_df_property('wastage_section', 'hidden', 1);
        } else {
            frm.set_df_property('wastage_section', 'hidden', 0);
        }

        if (frm.doc.workflow_state === "Under Production" || frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Add Strip Production Entry"), function() {
                frappe.new_doc('Strip Production Entry', {
                    strip_work_schedule: frm.doc.name
                });
            }).addClass("btn-primary");
        }
        
        if (frm.doc.docstatus === 1) {
            if (frm.doc.wastage_item) {
                frm.set_df_property('wastage_item', 'read_only', 1);
            }
            if (frm.doc.workflow_state === 'Job Complete') {
                frm.set_df_property('wastage_entries', 'read_only', 1);
            }
            setTimeout(() => {
                frm.page.clear_primary_action();
                frm.page.remove_inner_button('Amend');
            }, 100);
        }
        
        // Hide Cancel button if Production Entries exist
        if (frm.doc.docstatus === 1) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Strip Production Entry",
                    filters: { strip_work_schedule: frm.doc.name, docstatus: ["!=", 2] },
                    limit: 1
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        setTimeout(() => {
                            frm.page.remove_inner_btn('Cancel');
                        }, 100);
                    }
                }
            });
        }
    },
    
    warp_data_add: function(frm) {
        calculate_tensile_strength(frm);
    },
    
    warp_data_remove: function(frm) {
        calculate_tensile_strength(frm);
    },

    wastage_entries_remove: function(frm) {
        calculate_total_wastage(frm);
    }
});

frappe.ui.form.on("Strip Wastage Entry", {
    wastage_qty: function(frm) {
        calculate_total_wastage(frm);
    }
});

frappe.ui.form.on("Strip Yarn Data", {
    denier: function(frm) {
        calculate_tensile_strength(frm);
    },
    number_of_yarn: function(frm) {
        calculate_tensile_strength(frm);
    },
    denier_strength: function(frm) {
        calculate_tensile_strength(frm);
    }
});

function calculate_tensile_strength(frm) {
    let total_strength = 0;
    if (frm.doc.warp_data) {
        frm.doc.warp_data.forEach(row => {
            total_strength += (flt(row.denier) * flt(row.number_of_yarn) * flt(row.denier_strength));
        });
    }
    frm.set_value('strip_tensile_strength', total_strength);
    frm.set_value('strip_tensile_strength_kg', total_strength * 101.97);
}

function calculate_total_wastage(frm) {
    let total = 0;
    if (frm.doc.wastage_entries) {
        frm.doc.wastage_entries.forEach(row => {
            total += flt(row.wastage_qty);
        });
    }
    frm.set_value('wastage_qty', total);
}
