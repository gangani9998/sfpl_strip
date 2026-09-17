frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('📦 Dispatch Documents'), function() {
                frappe.call({
                    method: 'sfpl_strip.sfpl_strip.dispatch_documents.generate_dispatch_documents',
                    args: {
                        sales_invoice_name: frm.doc.name
                    },
                    callback: function(r) {
                        // The server returns the file as a download
                        if (!r.exc) {
                            frappe.msgprint(__('Dispatch Documents generated successfully!'));
                        }
                    }
                });
                
                // Trigger file download directly using window.open
                const url = "/api/method/sfpl_strip.sfpl_strip.dispatch_documents.generate_dispatch_documents?sales_invoice_name=" + encodeURIComponent(frm.doc.name);
                window.open(url, "_blank");
            }, __('Print'));
        }
    }
});
