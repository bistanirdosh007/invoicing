# invoicing/views.py
import pandas as pd
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.mail import EmailMessage
from django.shortcuts import render

def generate_pdf(invoice_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up some basic PDF elements
    p.drawString(100, 750, f"Invoice Number: {invoice_data['invoice_number']}")
    p.drawString(100, 730, f"Customer: {invoice_data['customer_name']}")
    p.drawString(100, 710, f"Date: {invoice_data['date']}")
    p.drawString(100, 690, f"Total Amount: ${invoice_data['total_amount']}")
    
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def send_invoice_email(pdf_buffer, customer_email, invoice_number, customer_name):
    subject = f"Invoice {invoice_number}"
    message = f"Dear {customer_name}, please find attached your invoice {invoice_number}."
    from_email = settings.EMAIL_HOST_USER

    # Create EmailMessage object
    email = EmailMessage(
        subject,
        message,
        from_email,
        [customer_email]
    )
    
    # Attach the generated PDF to the email
    email.attach(f"invoice_{invoice_number}.pdf", pdf_buffer.read(), "application/pdf")
    
    # Send the email with the attached PDF
    email.send(fail_silently=False)

def upload_invoice(request):
    if request.method == "POST" and request.FILES["invoice_file"]:
        # Read Excel file
        excel_file = request.FILES["invoice_file"]
        df = pd.read_excel(excel_file)

        for _, row in df.iterrows():
            # Create PDF from row data
            invoice_data = {
                "invoice_number": row["Invoice Number"],
                "customer_name": row["Customer Name"],
                "customer_email": row["Customer Email"],
                "date": row["Date"],
                "total_amount": row["Total Amount"],
            }
            
            # Generate PDF
            pdf_buffer = generate_pdf(invoice_data)
            
            # Send invoice email with attached PDF
            send_invoice_email(pdf_buffer, row["Customer Email"], row["Invoice Number"], row["Customer Name"])

        return HttpResponse("Invoices have been sent!", status=200)
    
    return render(request, "upload_invoice.html")
