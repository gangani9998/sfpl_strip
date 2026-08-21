// Copyright (c) 2026, Jay Kumar Gangani and contributors
// For license information, please see license.txt

frappe.ui.form.on("Strip Production Entry", {
    draw_sample_btn(frm) {
        let d = new frappe.ui.Dialog({
            title: 'Draw Sample',
            fields: [
                {
                    label: 'Sample Length (m)',
                    fieldname: 'sample_length',
                    fieldtype: 'Float',
                    reqd: 1
                },
                {
                    label: 'Sample Weight (kg)',
                    fieldname: 'sample_weight',
                    fieldtype: 'Float',
                    reqd: 1
                },
                {
                    label: 'Purpose',
                    fieldname: 'purpose',
                    fieldtype: 'Select',
                    options: ['Lab Testing', 'Customer Sample'],
                    reqd: 1
                }
            ],
            primary_action_label: 'Draw Sample',
            primary_action: function(values) {
                frappe.call({
                    method: 'sfpl_strip.sfpl_strip.doctype.strip_production_entry.strip_production_entry.make_sample_cut',
                    args: {
                        entry_name: frm.doc.name,
                        sample_length: values.sample_length,
                        purpose: values.purpose
                    },
                    freeze: true,
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(`Successfully created Stock Entry <a href="/app/stock-entry/${r.message}">${r.message}</a>`);
                            frm.reload_doc();
                            d.hide();
                        }
                    }
                });
            }
        });
        
        let get_gsm = () => flt(frm.doc.gsm) || 0;
        
        d.fields_dict.sample_length.$input.on('input', function() {
            if ($(this).is(':focus')) {
                let len = flt($(this).val());
                let gsm = get_gsm();
                let weight = (len * gsm) / 1000;
                // Format to 3 decimal places for kg
                d.set_value('sample_weight', parseFloat(weight.toFixed(3)));
            }
        });
        
        d.fields_dict.sample_weight.$input.on('input', function() {
            if ($(this).is(':focus')) {
                let weight = flt($(this).val());
                let gsm = get_gsm();
                if (gsm > 0) {
                    let len = (weight * 1000) / gsm;
                    // Format to 2 decimal places for meters
                    d.set_value('sample_length', parseFloat(len.toFixed(2)));
                }
            }
        });

        d.show();
    },

    process_qc_btn(frm) {
        let d = new frappe.ui.Dialog({
            title: 'Process QC / Scrap',
            fields: [
                {
                    label: 'Scrap Length (m)',
                    fieldname: 'scrap_length',
                    fieldtype: 'Float',
                    reqd: 1
                },
                {
                    label: 'Scrap Weight (kg)',
                    fieldname: 'scrap_weight',
                    fieldtype: 'Float',
                    reqd: 1
                },
                {
                    label: 'Defect Reason',
                    fieldname: 'defect_reason',
                    fieldtype: 'Data',
                    reqd: 1
                }
            ],
            primary_action_label: 'Process Scrap & Release',
            primary_action: function(values) {
                frappe.call({
                    method: 'sfpl_strip.sfpl_strip.doctype.strip_production_entry.strip_production_entry.process_qc_scrap',
                    args: {
                        entry_name: frm.doc.name,
                        scrap_length: values.scrap_length,
                        defect_reason: values.defect_reason
                    },
                    freeze: true,
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint("Successfully processed QC Scrap and released the remaining roll to Finished Goods.");
                            frm.reload_doc();
                            d.hide();
                        }
                    }
                });
            }
        });
        
        let get_gsm = () => flt(frm.doc.gsm) || 0;
        
        d.fields_dict.scrap_length.$input.on('input', function() {
            if ($(this).is(':focus')) {
                let len = flt($(this).val());
                let gsm = get_gsm();
                let weight = (len * gsm) / 1000;
                d.set_value('scrap_weight', parseFloat(weight.toFixed(3)));
            }
        });
        
        d.fields_dict.scrap_weight.$input.on('input', function() {
            if ($(this).is(':focus')) {
                let weight = flt($(this).val());
                let gsm = get_gsm();
                if (gsm > 0) {
                    let len = (weight * 1000) / gsm;
                    d.set_value('scrap_length', parseFloat(len.toFixed(2)));
                }
            }
        });

        d.show();
    },

    setup(frm) {
        // Fetch previous parameters on load if form is new
        if (frm.is_new() && frm.doc.strip_work_schedule) {
            fetch_previous_parameters(frm);
        }
    },
    strip_work_schedule(frm) {
        if (frm.doc.strip_work_schedule) {
            fetch_previous_parameters(frm);
        }
    },
    refresh(frm) {
        frm.toggle_enable('roll_net_weight', false);
        
        // Auto-fetch if draft has empty tables (recovering from old drafts)
        if (frm.doc.docstatus === 0 && frm.doc.strip_work_schedule) {
            if (!frm.doc.yarn_details || frm.doc.yarn_details.length === 0) {
                fetch_previous_parameters(frm);
            }
        }
        
        // Hide the raw text value of the barcode field since the SVG already has it
        let barcode_wrapper = frm.get_field('barcode').$wrapper;
        barcode_wrapper.find('.control-value').hide();
        barcode_wrapper.find('input').hide();
        
        // Hide the barcode entirely if it's a new, unsaved document
        if (frm.is_new()) {
            frm.set_df_property('barcode', 'hidden', 1);
        } else {
            frm.set_df_property('barcode', 'hidden', 0);
        }
        
        // Filter Product Code field to only show Items marked as Quality Item
        frm.set_query("strip_product_code", function () {
            return {
                filters: {
                    is_quality_item: 1
                }
            };
        });
        
        // Filter Work Schedule field to only show valid schedules
        frm.set_query("strip_work_schedule", function () {
            return {
                filters: {
                    docstatus: 1,
                    workflow_state: ["in", ["Under Production", "Under production"]]
                }
            };
        });
        
        if (!frm.is_new()) {
            frm.add_custom_button(__("Create Production Entry"), function() {
                frappe.model.with_doctype("Strip Production Entry", () => {
                    let doc = frappe.model.get_new_doc("Strip Production Entry");
                    doc.strip_work_schedule = frm.doc.strip_work_schedule;
                    frappe.set_route('Form', "Strip Production Entry", doc.name);
                });
            });

            if (frm.doc.docstatus === 1) {

                frm.add_custom_button(__("Open Batch"), function() {
                    frappe.set_route('Form', 'Batch', frm.doc.name);
                });
                
                frm.add_custom_button(__("Create MTC Strip"), function() {
                    let target_doctype = "MTC Strip";
                    
                    frappe.model.with_doctype(target_doctype, () => {
                        let mtc = frappe.model.get_new_doc(target_doctype);
                        mtc.lot_no = frm.doc.strip_work_schedule;
                        mtc.roll_no = frm.doc.name;
                        mtc.product_name = frm.doc.strip_product_code;
                        mtc.roll_width = frm.doc.actual_strip_width;
                        frappe.set_route('Form', target_doctype, mtc.name);
                    });
                }).addClass("btn-primary");
            }
        }
    },
    
    roll_gross_weight(frm) {
        calculate_net_weight(frm);
    },
    
    total_packaging_weight(frm) {
        calculate_net_weight(frm);
    },

    validate(frm) {
        if (flt(frm.doc.actual_strip_width) > 100) {
            frappe.msgprint({
                title: __('Validation Error'),
                indicator: 'red',
                message: __('Actual Strip Width (mm) cannot be greater than 100 mm.')
            });
            frappe.validated = false;
        }
        if (flt(frm.doc.roll_gross_weight) < 1) {
            frappe.msgprint({
                title: __('Validation Error'),
                indicator: 'red',
                message: __('Roll Gross Weight (kg) cannot be less than 1 kg.')
            });
            frappe.validated = false;
        }
        calculate_net_weight(frm);
        calculate_bom_weights(frm);
    }
});

function calculate_net_weight(frm) {
    let gross = flt(frm.doc.roll_gross_weight);
    let tube = flt(frm.doc.total_packaging_weight);
    
    if (gross > 50) {
        frappe.msgprint({
            title: __('Validation Error'),
            indicator: 'red',
            message: __('Roll Gross Weight cannot be greater than 50 kg.')
        });
        frappe.model.set_value(frm.doctype, frm.docname, 'roll_gross_weight', 0);
        gross = 0;
    }
    
    if (gross > 0 && tube > 0) {
        if ((tube / 1000) >= gross) {
            frappe.msgprint({
                title: __('Invalid Weight'),
                indicator: 'red',
                message: __('Total Packaging Weight cannot be greater than or equal to Roll Gross Weight.')
            });
            frappe.model.set_value(frm.doctype, frm.docname, 'total_packaging_weight', 0);
            return;
        }
        let net = gross - (tube / 1000);
        if (net < 0) net = 0;
        frm.set_value('roll_net_weight', net);
    } else {
        frm.set_value('roll_net_weight', gross);
    }
    
    let roll_length = flt(frm.doc.roll_length);
    let net = flt(frm.doc.roll_net_weight);
    if (roll_length > 0) {
        let gsm = (net / roll_length) * 1000;
        frm.set_value('gsm', gsm);
    } else {
        frm.set_value('gsm', 0);
    }
}

function calculate_bom_weights(frm) {
    let roll_length = flt(frm.doc.roll_length);
    let net_weight = flt(frm.doc.roll_net_weight);
    
    // Also recalculate GSM here just in case length changes but gross weight doesn't
    if (roll_length > 0) {
        let gsm = (net_weight / roll_length) * 1000;
        frm.set_value('gsm', gsm);
    } else {
        frm.set_value('gsm', 0);
    }
    
    // 1. Calculate Yarn Weights
    let total_yarn_weight = 0;
    if (frm.doc.yarn_details) {
        frm.doc.yarn_details.forEach(d => {
            // (Denier * Number of Yarn * 0.0001111 * Roll Length) / 1000 to get kg
            let row_weight = (flt(d.denier) * flt(d.number_of_yarn) * 0.0001111 * roll_length) / 1000;
            frappe.model.set_value(d.doctype, d.name, 'weight', row_weight);
            total_yarn_weight += row_weight;
        });
    }
    
    // 2. Calculate Coating Weights
    let total_coating_weight = net_weight - total_yarn_weight;
    if (total_coating_weight < 0) total_coating_weight = 0;
    
    if (frm.doc.coating_details) {
        frm.doc.coating_details.forEach(d => {
            let row_weight = total_coating_weight * (flt(d.ratio) / 100);
            frappe.model.set_value(d.doctype, d.name, 'weight', row_weight);
        });
    }
    
    frm.set_value('total_yarn_weight', total_yarn_weight);
    frm.set_value('total_coating_weight', total_coating_weight);
}

function fetch_previous_parameters(frm) {
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Strip Work Schedule",
            name: frm.doc.strip_work_schedule
        },
        callback: function(r) {
            if (r.message) {
                let ws = r.message;
                
                // Clear and populate Yarn Details
                frm.clear_table("yarn_details");
                if (ws.warp_data) {
                    ws.warp_data.forEach(d => {
                        let row = frm.add_child("yarn_details");
                        row.yarn = d.yarn;
                        row.denier = d.denier;
                        row.number_of_yarn = d.number_of_yarn;
                        row.denier_strength = d.denier_strength;
                    });
                }
                
                // Clear and populate Coating Details
                frm.clear_table("coating_details");
                if (ws.default_coating_ratios) {
                    ws.default_coating_ratios.forEach(d => {
                        let row = frm.add_child("coating_details");
                        row.coating_material = d.coating_material;
                        row.ratio = d.ratio;
                    });
                }
                
                frm.refresh_field("yarn_details");
                frm.refresh_field("coating_details");
                
                calculate_bom_weights(frm);
            }
        }
    });
    
    // Still fetch previous extrusion parameters
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Strip Production Entry",
            filters: {
                strip_work_schedule: frm.doc.strip_work_schedule
            },
            fields: [
                "barrel_z1", "barrel_z2", "barrel_z3", "barrel_z4", "barrel_z5",
                "die_z1", "die_z2", "extruder_rpm", "haul_off_rpm", "water_temp",
                "haul_off_temp", "haul_off_follower_rpm"
            ],
            order_by: "creation desc",
            limit: 1
        },
        callback: function(r) {
            if (r.message && r.message.length > 0) {
                let prev = r.message[0];
                for (let key in prev) {
                    if (!frm.doc[key]) {
                        frm.set_value(key, prev[key]);
                    }
                }
            }
        }
    });
}
