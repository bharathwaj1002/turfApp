from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User , auth
from .models import Booking
from django.views.decorators.http import require_POST
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
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

    # Convert the date string to a datetime object
    selected_date = datetime.strptime(date, '%Y-%m-%d').date()

    if not Booking.objects.filter(date=selected_date, session=session).exists():
        # Redirect to the confirm_booking page with the input data
        return redirect('confirm_booking', name=name, date=selected_date, session=session, mobile_number=mobile_number)
    else:
        return HttpResponse(f"Sorry, the turf is not available for {name} on {date} ({session}).")



def confirm_booking(request, name, date, session, mobile_number):
    selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    booking = None

    if request.method == 'POST':
        booking = Booking.objects.create(name=name, date=selected_date, session=session, mobile_number=mobile_number)
        return redirect('complete_booking', booking_id=booking.pk)

    return render(request, 'confirm_booking.html', {'booking': booking, 'name': name, 'date': date, 'session': session, 'mobile_number': mobile_number})



def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    booking_details = f"Name: {booking.name}\nDate: {booking.date}\nSession: {booking.session}\nMobile Number: {booking.mobile_number}"
    qr.add_data(booking_details)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(f"booking_qr_{booking_id}.png")
    return render(request, 'complete_booking.html', {'booking': booking, 'qr_img': qr_img})



def cancel_booking(request):
    return redirect('index')


    
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def view_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'view_bookings.html', {'bookings': bookings})



@login_required
def admin_home(request):
    # Redirect authenticated admin users to the home page
    if request.user.is_staff:
        return redirect('index')  # Update 'home' with the actual URL name for your home page
    else:
        # Redirect non-admin users to an appropriate page or handle as needed
        return redirect('index')
    
    
    
def logout(request):
    auth.logout(request)
    return redirect('/')