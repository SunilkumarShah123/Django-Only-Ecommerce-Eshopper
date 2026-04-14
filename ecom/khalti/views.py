from django.shortcuts import render,get_object_or_404,redirect
from .models import Transaction

from io import BytesIO
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage

import uuid
import requests
from app.models import Order    
from django.http import JsonResponse
import json

# Create your views here.
def initiate_khalti_payment(request,id): 
        data=get_object_or_404(Order,id=id)
        url = "https://dev.khalti.com/api/v2/epayment/initiate/"
        payload = json.dumps({
            "return_url": "http://127.0.0.1:8000/khalti/verify-khalti/",
            "website_url": "http://127.0.0.1:8000/khalti/verify-khalti/",
            "amount": int(float(data.total)) * 100,
            'transaction_id': str(uuid.uuid4()),
            "purchase_order_id": data.id,
            "purchase_order_name": data.product,
            "customer_info": {
            "name": data.full_name,
            "email": data.email,
            "phone": data.phone
            }
        })
        headers = {
            'Authorization': 'key 553e1a869ebb4491a02dba4139c03339',
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

        payment_data = json.loads(response.text)['payment_url']
        return redirect(payment_data)


def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    
    if request.method == 'GET':
        headers = {
            'Authorization': 'key 553e1a869ebb4491a02dba4139c03339',
            'Content-Type': 'application/json',
        }
        
        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
        purchase_order_id = request.GET.get('purchase_order_id')
        
        data = json.dumps({
            'pidx': pidx
        })

        res = requests.request('POST', url, headers=headers, data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)

     
        if new_res['status'] == 'Completed':
            order = get_object_or_404(Order, id=purchase_order_id)
            order.is_pay = True
            order.save()
             
            Transaction.objects.create(
                order=order,
                transaction_id=transaction_id,
                amount=order.total,
                user=request.user.username
            ) 
            
            #automatic pdf generation based on order and transaction details
            pdf_buffer = BytesIO()
            p = canvas.Canvas(pdf_buffer)
            p.drawString(100, 800, "Order Confirmation")
            p.drawString(100, 780, f"Order ID: {order.id}")
            p.drawString(100, 760, f"Product: {order.product}")
            p.drawString(100, 740, f"Quantity: {order.quantity}")
            p.drawString(100, 720, f"Total Amount: {order.total}")
            p.drawString(100, 700, "Thank you for your purchase!")
            p.showPage()
            p.save()
            pdf_buffer.seek(0)


            #email with pdf attachment
            subject = 'Order Confirmation - Your Order has been Placed!'
            message = f'Dear {order.full_name},\n\nThank you for your order!\n\nYour order for {order.product} has been successfully placed. We will notify you once it is shipped.\n\nOrder Details:\nProduct: {order.product}\nQuantity: {order.quantity}\nTotal Amount: RS.{order.total}\n\nThank you for shopping with us!\n\nBest regards,\nEcom Team'
            from_email = "nirpatidevi123@gmail.com"
            recepient_email = order.email
            pdf_name=f"{order.full_name}_Product_{order.product}_Order_{order.id}_.pdf"
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=[recepient_email]
            )
            email.attach(pdf_name, pdf_buffer.getvalue(), 'application/pdf')
            pdf_buffer.close()
            
            email.send()
            return redirect('profile')
        else:
            print("Payment verification failed. Khalti response:", json.dumps(new_res, indent=4))
            return JsonResponse({'error': 'Payment verification failed'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)