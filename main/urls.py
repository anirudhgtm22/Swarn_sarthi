# urls.py

from django.urls import path
from .views import index,PlaceOrderView , about_us, update_profile
from . import views
from .views import RegistrationAPIView, LoginAPIView , UserProfileUpdateView ,ServicesAPIView , get_services , submit_order , book_orders,profile, YourProtectedView
from django.contrib import admin

admin.site.site_header = 'Swarn Sarthi '                  
admin.site.index_title = 'Swarn Sarthi administration'                 
admin.site.site_title = 'Swarn Sarthi Admin Panel'

urlpatterns = [
    path('', index, name='index'),
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'), 
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('send-otp/',views.send_otp),
    path('verify-otp/',views.verify_otp,name="verify-otp"),
    path('about-us/',views.about_us,name="about-us"),
    path('login-signup/',views.login_signup,name="login-signup"),
    path('contact-us/',views.contact_us,name="contact-us"),
    path('services',ServicesAPIView.as_view(),name='service'),
    path('get_services/', get_services, name='get_services'),
    path('submit_order/', submit_order, name='submit_order'),
    path('book-now/', book_orders, name='book-now'),
    path('profile/', profile, name='profile'),
    path('api/token/refresh/',YourProtectedView.as_view(), name='token_refresh'),
    path('update_profile/', update_profile, name='update_profile'),
]  
 
  