from django.shortcuts import render
from django.http import HttpResponse
from .models import Booking
from django.views.decorators.http import require_POST
from datetime import datetime

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

    # Convert the date string to a datetime object
    selected_date = datetime.strptime(date, '%d-%m-%Y').date()

    # Check availability in the database
    if not Booking.objects.filter(date=selected_date, session=session).exists():
        # Turf is available, save the booking details in the database
        Booking.objects.create(name=name, date=selected_date, session=session)
        return HttpResponse(f"Booking successful for {name} on {date} ({session})")
    else:
        # Turf is not available on the selected date and session
        return HttpResponse(f"Sorry, the turf is not available for {name} on {date} ({session}).")