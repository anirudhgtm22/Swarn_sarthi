# orders/utils.py
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.pdfgen import canvas

def generate_invoice(order_details, output_filename):
    print("u1")
    pdf_canvas = canvas.Canvas(output_filename)
    pdf_canvas.drawString(100, 800, f"Order ID: {order_details['order_id']}")
    pdf_canvas.drawString(100, 780, f"Total Amount: ${order_details['total_amount']}")
    pdf_canvas.save()
 
def send_invoice_email(to_email, invoice_pdf_path):
    print("u2") 
    subject = 'Invoice for Your Order'
    message = 'Thank you for your order! Please find the attached invoice.'
    from_email = settings.EMAIL_HOST_USER 
    print("1",subject,message,from_email,[to_email])
    print("2",invoice_pdf_path)
    email = EmailMessage(subject, message, from_email, [to_email])
    print("3")
    email.attach_file(invoice_pdf_path)
    print("4")
    email.send()
    print("5")

from datetime import datetime

def generate_invoice_number():
    current_datetime = datetime.now()
    day = str(current_datetime.day).zfill(2)
    month = str(current_datetime.month).zfill(2)
    hour = str(current_datetime.hour).zfill(2)
    return f'INV-{day}{month}-{hour}'
