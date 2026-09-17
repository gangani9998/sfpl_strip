import frappe
from frappe.utils.pdf import get_pdf
import zipfile
import io

@frappe.whitelist()
def generate_dispatch_documents(sales_invoice_name):
    # 1. Generate Sales Invoice PDF
    try:
        doc = frappe.get_doc("Sales Invoice", sales_invoice_name)
    except frappe.DoesNotExistError:
        frappe.throw(f"Sales Invoice {sales_invoice_name} not found")

    pdfs = []
    
    si_html = frappe.get_print("Sales Invoice", sales_invoice_name, print_format="Shivoham Sales Invoice", as_pdf=False)
    pdfs.append({"name": f"Sales_Invoice_{sales_invoice_name}.pdf", "content": get_pdf(si_html)})
    
    # 2. Find Delivery Notes connected to this Sales Invoice
    delivery_notes = set()
    for item in doc.items:
        if item.delivery_note:
            delivery_notes.add(item.delivery_note)
            
    # 3. Process Delivery Notes
    batch_nos = set()
    for dn_name in delivery_notes:
        dn_doc = frappe.get_doc("Delivery Note", dn_name)
        # Using a fallback print format if "Packing List" doesn't exist just in case
        try:
            dn_html = frappe.get_print("Delivery Note", dn_name, print_format="Packing List", as_pdf=False)
        except Exception:
            dn_html = frappe.get_print("Delivery Note", dn_name, as_pdf=False)
            
        pdfs.append({"name": f"Packing_List_{dn_name}.pdf", "content": get_pdf(dn_html)})
        
        for item in dn_doc.items:
            if item.serial_and_batch_bundle:
                bundle = frappe.get_doc("Serial and Batch Bundle", item.serial_and_batch_bundle)
                for entry in bundle.entries:
                    if entry.batch_no:
                        batch_nos.add(entry.batch_no)
                        
    # 4. Find MTCs for these Batches
    # A Batch has 'strip_work_schedule'. MTC Strip is linked to 'strip_work_schedule' via 'lot_no'.
    for batch_no in batch_nos:
        batch_doc = frappe.get_doc("Batch", batch_no)
        work_schedule = batch_doc.get("strip_work_schedule")
        if work_schedule:
            # Check MTC Strip
            mtcs = frappe.get_all("MTC Strip", filters={"lot_no": work_schedule, "docstatus": 1}, pluck="name")
            for mtc_name in mtcs:
                mtc_html = frappe.get_print("MTC Strip", mtc_name, print_format="MTC Strip", as_pdf=False)
                pdfs.append({"name": f"MTC_Strip_{mtc_name}.pdf", "content": get_pdf(mtc_html)})
                
            # Check SFUG MTC
            if frappe.db.exists("DocType", "SFUG MTC"):
                sfug_mtcs = frappe.get_all("SFUG MTC", filters={"lot_no": work_schedule, "docstatus": 1}, pluck="name")
                for mtc_name in sfug_mtcs:
                    mtc_html = frappe.get_print("SFUG MTC", mtc_name, print_format="SFUG MTC", as_pdf=False)
                    pdfs.append({"name": f"SFUG_MTC_{mtc_name}.pdf", "content": get_pdf(mtc_html)})
                
            # Check SFBG MTC
            if frappe.db.exists("DocType", "SFBG MTC"):
                sfbg_mtcs = frappe.get_all("SFBG MTC", filters={"lot_no": work_schedule, "docstatus": 1}, pluck="name")
                for mtc_name in sfbg_mtcs:
                    mtc_html = frappe.get_print("SFBG MTC", mtc_name, print_format="SFBG MTC", as_pdf=False)
                    pdfs.append({"name": f"SFBG_MTC_{mtc_name}.pdf", "content": get_pdf(mtc_html)})

    # 5. Create ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for pdf in pdfs:
            zip_file.writestr(pdf["name"], pdf["content"])
            
    frappe.response['filename'] = f"Dispatch_Documents_{sales_invoice_name}.zip"
    frappe.response['filecontent'] = zip_buffer.getvalue()
    frappe.response['type'] = 'download'
