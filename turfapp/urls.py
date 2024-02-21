from django.urls import path
from .import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


@require_http_methods(["GET"])
@csrf_exempt
def csrf_token(request):
    return JsonResponse({'csrfToken': 'your_csrf_token'}, status=200)

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('about-us',views.about,name='about-us'),
    path('contacts',views.contacts,name='contacts'),
    path('check_availability', views.check_availability, name='check_availability'),
    path('confirm_booking/<str:name>/<slug:date>/<str:session>/<str:mobile_number>/<str:email>/', views.confirm_booking, name='confirm_booking'),
    path('complete_booking/<int:booking_id>', views.complete_booking, name='complete_booking'),
    path('handle_razorpay_payment/<str:name>/<slug:date>/<str:session>/<str:mobile_number>/<str:email>/',views.handle_razorpay_payment,name='handle_razorpay_payment'),
    path('payment_failed', views.payment_failed, name='payment_failed'),
    path('turf_incharge_verification/', views.turf_incharge_verification, name='turf_incharge_verification'),
    path('verify_booking/<str:booking_data>/', views.verify_booking, name='verify_booking'),
    path('turf_incharge_verification_automated/', views.turf_incharge_verification_automated, name='turf_incharge_verification_automated'),
    path('cancel_booking', views.cancel_booking, name='cancel_booking'),
    path('view_bookings', views.view_bookings, name='view_bookings'),
    path('logout', views.logout, name='logout'),
    path('csrf/', csrf_token),
]