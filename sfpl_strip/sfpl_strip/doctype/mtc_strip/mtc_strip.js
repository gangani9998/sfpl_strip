// Copyright (c) 2026, Jay Kumar Gangani and contributors
// For license information, please see license.txt

frappe.ui.form.on("MTC Strip", {
    refresh(frm) {
        
    },
    validate(frm) {
        calculate_means(frm);
    }
});

frappe.ui.form.on("U Specimen Data", {
    tensile_strenth: function(frm, cdt, cdn) {
        calculate_means(frm);
    },
    elongation_at_designeted: function(frm, cdt, cdn) {
        calculate_means(frm);
    },
    elongation_at_ultimate: function(frm, cdt, cdn) {
        calculate_means(frm);
    },
    specimen_data_remove: function(frm) {
        calculate_means(frm);
    }
});

function calculate_means(frm) {
    let total_ts = 0;
    let total_ed = 0;
    let total_eu = 0;
    let count = 0;
    
    if (frm.doc.specimen_data && frm.doc.specimen_data.length > 0) {
        frm.doc.specimen_data.forEach(d => {
            total_ts += flt(d.tensile_strenth);
            total_ed += flt(d.elongation_at_designeted);
            total_eu += flt(d.elongation_at_ultimate);
            count++;
        });
    }
    
    if (count > 0) {
        frm.set_value("mean_tensile_strength", total_ts / count);
        frm.set_value("mean_elongation_designated", total_ed / count);
        frm.set_value("mean_elongation_ultimate", total_eu / count);
    } else {
        frm.set_value("mean_tensile_strength", 0);
        frm.set_value("mean_elongation_designated", 0);
        frm.set_value("mean_elongation_ultimate", 0);
    }
}
