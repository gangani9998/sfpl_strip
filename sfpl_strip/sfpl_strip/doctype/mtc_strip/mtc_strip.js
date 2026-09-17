// Copyright (c) 2026, Jay Kumar Gangani and contributors
// For license information, please see license.txt

frappe.ui.form.on("MTC Strip", {
    refresh(frm) {
        toggle_tables_based_on_product(frm);
    },
    validate(frm) {
        calculate_means(frm);
    },
    product_name(frm) {
        toggle_tables_based_on_product(frm);
    }
});

function toggle_tables_based_on_product(frm) {
    if (frm.doc.product_name) {
        frappe.db.get_value('Item', frm.doc.product_name, 'item_group', (r) => {
            if (r && r.item_group) {
                let group = r.item_group.toLowerCase();
                let is_pack_strap = group.includes('pack') || group.includes('strap');
                
                // If the group explicitly includes 'geo', it is not packstrap
                if (group.includes('geo')) {
                    is_pack_strap = false;
                }

                // 1. Both products get Specimen Data (for Tensile tests)
                frm.set_df_property('specimen_data', 'hidden', 0);
                
                if (frm.fields_dict['specimen_data'] && frm.fields_dict['specimen_data'].grid) {
                    frm.fields_dict['specimen_data'].grid.update_docfield_property('elongation_at_designeted', 'hidden', is_pack_strap ? 1 : 0);
                    frm.fields_dict['specimen_data'].grid.update_docfield_property('elongation_at_ultimate', 'hidden', is_pack_strap ? 1 : 0);
                    frm.fields_dict['specimen_data'].grid.reset_grid();
                }

                if (is_pack_strap) {
                    // Pack strap -> Show System Strength Data table and summary field
                    frm.set_df_property('system_strength_data', 'hidden', 0);
                    frm.set_df_property('mean_elongation_designated', 'hidden', 1);
                    frm.set_df_property('mean_elongation_ultimate', 'hidden', 1);
                    frm.set_df_property('mean_system_strength', 'hidden', 0);
                } else {
                    // GeoStrap -> Hide System Strength Data, show elongation summary
                    frm.set_df_property('system_strength_data', 'hidden', 1);
                    frm.set_df_property('mean_elongation_designated', 'hidden', 0);
                    frm.set_df_property('mean_elongation_ultimate', 'hidden', 0);
                    frm.set_df_property('mean_system_strength', 'hidden', 1);
                }
                
                frm.refresh_field('specimen_data');
            }
        });
    } else {
        // Show both if product not selected yet, but hide means
        frm.set_df_property('specimen_data', 'hidden', 0);
        frm.set_df_property('system_strength_data', 'hidden', 0);
        frm.set_df_property('mean_system_strength', 'hidden', 1);
        frm.refresh_field('specimen_data');
    }
}

frappe.ui.form.on("U Specimen Data", {
    tensile_strenth: function(frm, cdt, cdn) { calculate_means(frm); },
    elongation_at_designeted: function(frm, cdt, cdn) { calculate_means(frm); },
    elongation_at_ultimate: function(frm, cdt, cdn) { calculate_means(frm); },
    specimen_data_remove: function(frm) { calculate_means(frm); }
});

frappe.ui.form.on("Strip System Strength Data", {
    system_strength: function(frm, cdt, cdn) { calculate_means(frm); },
    system_strength_data_remove: function(frm) { calculate_means(frm); }
});

function calculate_means(frm) {
    // 1. Calculate U Specimen Data (GeoStrap & Packstrap Tensile Tests)
    let total_ts_1 = 0, total_ed = 0, total_eu = 0, count_1 = 0;
    
    if (frm.doc.specimen_data && frm.doc.specimen_data.length > 0) {
        frm.doc.specimen_data.forEach(d => {
            total_ts_1 += flt(d.tensile_strenth);
            total_ed += flt(d.elongation_at_designeted);
            total_eu += flt(d.elongation_at_ultimate);
            count_1++;
        });
    }
    
    if (count_1 > 0) {
        frm.set_value("mean_tensile_strength", total_ts_1 / count_1);
        frm.set_value("mean_elongation_designated", total_ed / count_1);
        frm.set_value("mean_elongation_ultimate", total_eu / count_1);
    } else {
        frm.set_value("mean_tensile_strength", 0);
        frm.set_value("mean_elongation_designated", 0);
        frm.set_value("mean_elongation_ultimate", 0);
    }

    // 2. Calculate System Strength Data (Packstrap only)
    let total_ss = 0, count_2 = 0;

    if (frm.doc.system_strength_data && frm.doc.system_strength_data.length > 0) {
        frm.doc.system_strength_data.forEach(d => {
            total_ss += flt(d.system_strength);
            count_2++;
        });
    }

    if (count_2 > 0) {
        frm.set_value("mean_system_strength", total_ss / count_2);
    } else {
        frm.set_value("mean_system_strength", 0);
    }
}
