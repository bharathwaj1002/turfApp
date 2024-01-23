from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User , auth
from .models import Booking
from django.views.decorators.http import require_POST
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files import File
import qrcode

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
        return HttpResponse(f"Sorry, the turf is not available for {name} on {date} ({session}).")



def confirm_booking(request, name, date, session, mobile_number, email):
    selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    booking = None

    if request.method == 'POST':
        booking = Booking.objects.create(name=name, date=selected_date, session=session, mobile_number=mobile_number, email=email)
        return redirect('complete_booking', booking_id=booking.pk)

    return render(request, 'confirm_booking.html', {'booking': booking, 'name': name, 'date': date, 'session': session, 'mobile_number': mobile_number, 'email':email})



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
    from io import BytesIO
    qr_img_io = BytesIO()
    qr_img.save(qr_img_io, format='PNG')
    qr_img_io.seek(0)

    # Create and email
    subject = 'Booking Confirmation'
    to_email = [booking.email]  # Replace with the actual field name storing the customer's email

    # Render email template
    html_message = render_to_string('booking_confirmation_email.html', {'booking': booking})
    plain_message = strip_tags(html_message)

    # Create email
    email = EmailMessage(subject, plain_message, to=to_email)

    # Attach QR code to email
    email.attach('booking_qr.png', qr_img_io.read(), 'image/png')

    # Send email
    email.send()

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




def handle_500(request):
    error_message = "Uh oh, the cosmos just hiccupped!"
    distorted_quote = "Just remember, when you’re feeling very small and insignificant, remember something enormous is at work in you all the time: your DNA code. Each molecule is a piece of a star story.” - Neil deGrasse Tyson"
    context = {
        "error_message": error_message,
        "distorted_quote": distorted_quote,
    }
    return render(request, "500.html", context)