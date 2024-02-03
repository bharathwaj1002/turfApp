from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User , auth
from .models import Booking
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from turfproject.settings import RAZORPAY_API_KEY, RAZORPAY_SECRET
from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files import File
import qrcode
import razorpay
import logging
from django.urls import reverse
from django.http import JsonResponse
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request,'index.html')



def about(request):
    return render(request,'about-us.html')



def contacts(request):
    return render(request,'contacts.html')



@require_POST
def check_availability(request):
    name = request.POST.get('name')
    date = request.POST.get('date')
    session = request.POST.get('session')
    mobile_number = request.POST.get('mobile_number')
    email = request.POST.get('email')
    selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    if not Booking.objects.filter(date=selected_date, session=session).exists():
        return redirect('confirm_booking', name=name, date=selected_date, session=session, mobile_number=mobile_number, email=email)
    else:
        return redirect('no_availability', name=name, date=selected_date, session=session)



def no_availability(request, name, date, session):
    context = {
         'name': name,
         'date': date,
         'session': session
    }
    return render(request,'no_availability.html', context)



client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_SECRET))
def confirm_booking(request, name, date, session, mobile_number, email):
    data = {
    "amount": 50000,
    "currency": "INR",
    "payment_capture": "1"
}
    payment_order = client.order.create(data=data)
    order_id = payment_order['id']
    
    context = {
         'name': name,
         'date': date,
         'session': session,
         'mobile_number': mobile_number,
         'email': email,
         'amount': 500,
         'api_key': RAZORPAY_API_KEY,
         'order_id': order_id
    }
    return render(request, 'confirm_booking.html',context)



def verify_razorpay_payment(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    razorpay_key_id = RAZORPAY_API_KEY
    razorpay_key_secret = RAZORPAY_SECRET

    client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

    try:
        # Verify the payment
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        }

        client.utility.verify_payment_signature(params_dict)

        # Payment verification successful
        return True

    except Exception as e:
        return False
    
    
    
@csrf_exempt
def handle_razorpay_payment(request,name, date, session, mobile_number, email):
    if request.method == 'POST':
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        
        if verify_razorpay_payment(razorpay_order_id, razorpay_payment_id, razorpay_signature):  
            selected_date = datetime.strptime(date, '%Y-%m-%d').date()          
            booking = Booking.objects.create(name=name, date=selected_date, session=session, mobile_number=mobile_number, email=email)
            
            
            return redirect('complete_booking', booking_id=booking.pk)
    return JsonResponse({'status': 'error'})



def payment(request):
    return render(request, 'payment.html')




def payment_failed(request):
    return render(request, 'payment_failed.html')



def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5,
    )
    qr.add_data(f"Booking ID: {booking.id}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to BytesIO for attaching to the email
    qr_img_io = BytesIO()
    qr_img.save(qr_img_io, format='PNG')
    qr_img_io.seek(0)

    # Create and email
    subject = 'Booking Confirmation'
    to_email = [booking.email,'b22203005@gmail.com']  # Replace with the actual field name storing the customer's email

    # Render email template
    html_message = render_to_string('booking_confirmation_email.html', {'booking': booking})
    plain_message = strip_tags(html_message)

    # Create email
    email = EmailMessage(subject, plain_message, to=to_email)

    # Attach QR code to email
    email.attach('booking_qr.png', qr_img_io.read(), 'image/png')

    # Send email
    #email.send()

    return render(request, 'complete_booking.html', {'booking': booking})



def turf_incharge_verification(request):
    return render(request, 'turf_incharge_verification.html')



def verify_booking(request, booking_data):
    try:
        booking_id = int(booking_data.split(":")[1].strip())
        booking = Booking.objects.get(id=booking_id)
        return render(request, 'verification_result.html', {'booking': booking})
    except Booking.DoesNotExist:
        return render(request, 'verification_result.html', {'booking_not_found': True})
    
    
    
def turf_incharge_verification_automated(request):
    return render(request, 'turf_incharge_verification_automated.html')



def cancel_booking(request):
    return redirect('index')


    
def is_superuser(user):
    return user.is_superuser



@user_passes_test(is_superuser)
def view_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'view_bookings.html', {'bookings': bookings})



@user_passes_test(is_superuser)
def turf_incharge_verification(request):
    return render(request,'turf_incharge_verification.html')
    
    
    
def logout(request):
    auth.logout(request)
    return redirect('/')