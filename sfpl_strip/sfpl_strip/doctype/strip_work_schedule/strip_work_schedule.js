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
        
        // Add Polymer Calculator Button
        frm.add_custom_button(__("Polymer Calculator"), function() {
            if (!frm.doc.default_coating_ratios || frm.doc.default_coating_ratios.length === 0) {
                frappe.msgprint(__("No coating polymer ratio data found in BOM."));
                return;
            }

            let item_codes = frm.doc.default_coating_ratios.map(r => r.coating_material).filter(Boolean);
            
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Item',
                    filters: { name: ['in', item_codes] },
                    fields: ['name', 'item_name']
                },
                callback: function(r) {
                    let item_names = {};
                    if (r.message) {
                        r.message.forEach(item => {
                            item_names[item.name] = item.item_name;
                        });
                    }
                    show_calculator(item_names);
                }
            });

            function show_calculator(item_names) {
                let fields = [
                    {
                        label: 'Total Batch Size (Kg)',
                        fieldname: 'batch_size',
                        fieldtype: 'Float',
                        reqd: 1,
                        default: 500
                    },
                    {
                        fieldname: 'html_results',
                        fieldtype: 'HTML'
                    }
                ];

                let d = new frappe.ui.Dialog({
                    title: __("Polymer Batch Calculator"),
                    fields: fields,
                    size: 'large',
                    primary_action_label: __("Close"),
                    primary_action: function() {
                        d.hide();
                    }
                });

                let is_updating = false;

                function render_table() {
                    let html = `
                        <style>
                            .req-kg-input::-webkit-outer-spin-button,
                            .req-kg-input::-webkit-inner-spin-button {
                                -webkit-appearance: none;
                                margin: 0;
                            }
                            .req-kg-input {
                                -moz-appearance: textfield;
                            }
                        </style>
                        <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Coating Material</th>
                                <th>Ratio (%)</th>
                                <th>Required (Kg)</th>
                            </tr>
                        </thead>
                        <tbody>`;
                    
                    frm.doc.default_coating_ratios.forEach((row, idx) => {
                        let display_name = item_names[row.coating_material] || row.coating_material || "";
                        html += `<tr>
                            <td style="vertical-align: middle;">${display_name}</td>
                            <td style="vertical-align: middle;">${row.ratio || 0}%</td>
                            <td style="padding: 5px;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <input type="number" class="form-control req-kg-input" data-ratio="${row.ratio || 0}" style="text-align: right; flex: 1;">
                                    <span style="font-weight: 500;">Kg</span>
                                </div>
                            </td>
                        </tr>`;
                    });
                    
                    html += `</tbody></table>`;
                    d.fields_dict.html_results.$wrapper.html(html);

                    // Bind reverse calculation events (Live typing in rows)
                    d.fields_dict.html_results.$wrapper.find('.req-kg-input').on('input', function(e) {
                        if (is_updating) return;
                        
                        let req_kg = flt($(this).val());
                        let ratio = flt($(this).attr('data-ratio'));
                        
                        if (ratio > 0) {
                            is_updating = true;
                            let total_batch = req_kg / (ratio / 100);
                            
                            // Update Total Batch Size field
                            d.get_field('batch_size').set_value(total_batch);
                            
                            // Update all other inputs
                            d.fields_dict.html_results.$wrapper.find('.req-kg-input').each(function() {
                                if (this !== e.target) {
                                    let r = flt($(this).attr('data-ratio'));
                                    let val = total_batch * (r / 100);
                                    $(this).val(flt(val, 2));
                                }
                            });
                            is_updating = false;
                        }
                    });
                }

                function handle_batch_change() {
                    if (is_updating) return;
                    is_updating = true;
                    
                    let batch = flt(d.get_value('batch_size'));
                    d.fields_dict.html_results.$wrapper.find('.req-kg-input').each(function() {
                        let ratio = flt($(this).attr('data-ratio'));
                        let val = batch * (ratio / 100);
                        $(this).val(flt(val, 2));
                    });
                    
                    is_updating = false;
                }

                // Render UI
                render_table();
                
                // Live update for total batch size typing
                d.fields_dict.batch_size.$input.on('input', handle_batch_change);
                d.fields_dict.batch_size.df.onchange = handle_batch_change;

                // Trigger initial calculation
                handle_batch_change();
                
                d.show();
            }
        });
        
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
