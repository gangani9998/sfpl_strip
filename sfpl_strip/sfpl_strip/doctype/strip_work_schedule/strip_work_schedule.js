// Copyright (c) 2026, Jay Kumar Gangani and contributors
// For license information, please see license.txt

frappe.ui.form.on("Strip Work Schedule", {
    refresh(frm) {
        if (!frm.doc.created_on) {
            frm.set_value('created_on', frm.doc.creation || frappe.datetime.now_datetime());
        }
        
        // Force dashboard connections to display side-by-side to save vertical space
        setTimeout(() => {
            if (frm.dashboard.wrapper) {
                frm.dashboard.wrapper.find('.document-link').parent().css({
                    'display': 'flex',
                    'flex-wrap': 'wrap',
                    'gap': '15px'
                });
                frm.dashboard.wrapper.find('.document-link').css({
                    'flex': '1 1 calc(50% - 15px)',
                    'margin-bottom': '0'
                });
            }
        }, 500);
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
        
        // Hide wastage section if the schedule is in Draft (Drawing) state
        if (frm.doc.docstatus === 0) {
            frm.set_df_property('wastage_section', 'hidden', 1);
        } else {
            frm.set_df_property('wastage_section', 'hidden', 0);
        }

        if (frm.doc.workflow_state === "Under Production" || frm.doc.workflow_state === "Under production") {
            frm.add_custom_button(__("Add Strip Production Entry"), function() {
                frappe.new_doc('Strip Production Entry', {
                    strip_work_schedule: frm.doc.name
                });
            }).addClass("btn-primary");
        }
        
        if (frm.doc.docstatus === 2) {
            setTimeout(() => {
                frm.page.clear_primary_action();
                frm.page.remove_inner_button('Amend');
            }, 100);
        }
        
        if (frm.doc.docstatus === 1) {
            if (frm.doc.workflow_state !== 'Under Production' && frm.doc.workflow_state !== 'Under production') {
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
    
    before_workflow_action: function(frm) {
        if (frm.selected_workflow_action === 'Complete Job' || frm.selected_workflow_action === 'Job Complete') {
            let total = 0;
            if (frm.doc.wastage_entries) {
                frm.doc.wastage_entries.forEach(row => {
                    total += flt(row.wastage_qty);
                });
            }
            if (total <= 0) {
                frappe.dom.unfreeze(); // Unfreeze the UI so the user can interact with the prompt
                return new Promise((resolve, reject) => {
                    frappe.prompt([
                        {
                            label: 'Wastage Qty (kg)',
                            fieldname: 'wastage_qty',
                            fieldtype: 'Float',
                            reqd: 1
                        },
                        {
                            label: 'Reason',
                            fieldname: 'reason',
                            fieldtype: 'Select',
                            options: 'Startup\nBreakdown\nMaterial Shortage\nPower Cut\nOther',
                            reqd: 1
                        }
                    ], (values) => {
                        frappe.dom.freeze("Saving Wastage Data...");
                        let row = frm.add_child('wastage_entries');
                        row.wastage_qty = values.wastage_qty;
                        row.reason = values.reason;
                        frm.refresh_field('wastage_entries');
                        frm.save().then(() => {
                            resolve(); 
                        }).catch(() => {
                            reject();
                        });
                    }, 'Please Enter Wastage Data', 'Submit \u0026 Complete Job', () => {
                        // On Cancel
                        frappe.msgprint("Wastage entry is required to complete the job.");
                        reject();
                    });
                });
            }
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
    },
    
    mixing_batch_size: function(frm) {
        if (frm.doc.mixing_batch_size && frm.doc.default_coating_ratios) {
            let batch = flt(frm.doc.mixing_batch_size);
            frm.doc.default_coating_ratios.forEach(d => {
                let qty = batch * (flt(d.ratio) / 100);
                frappe.model.set_value(d.doctype, d.name, 'qty_kg', qty);
            });
        }
    }
});

frappe.ui.form.on("Strip Wastage Entry", {
    wastage_qty: function(frm) {
        calculate_total_wastage(frm);
    }
});

frappe.ui.form.on("Strip Coating Ratio", {
    qty_kg: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.qty_kg && row.ratio) {
            let total_batch = flt(row.qty_kg) / (flt(row.ratio) / 100);
            frm.set_value('mixing_batch_size', total_batch);
            
            // Recalculate other rows
            frm.doc.default_coating_ratios.forEach(d => {
                if (d.name !== row.name) {
                    let qty = total_batch * (flt(d.ratio) / 100);
                    frappe.model.set_value(d.doctype, d.name, 'qty_kg', qty);
                }
            });
        }
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
            total_strength += (flt(row.denier) * flt(row.number_of_yarn) * (flt(row.denier_strength) / 100000));
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
