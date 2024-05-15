# # urls.py

# from django.urls import path
# from .views import index,PlaceOrderView , about_us, update_profile
# from . import views
# from .views import RegistrationAPIView, LoginAPIView , UserProfileUpdateView ,ServicesAPIView, submit_order , book_orders,profile, YourProtectedView, ServicesViewSet
# from django.contrib import admin
# from rest_framework.routers import DefaultRouter

# admin.site.site_header = 'Swarn Sarthi '                  
# admin.site.index_title = 'Swarn Sarthi administration'                 
# admin.site.site_title = 'Swarn Sarthi Admin Panel'

# router = DefaultRouter()
# router.register(r'services', ServicesViewSet)

# urlpatterns = [
#     path('', index, name='index'),
#     path('place_order/', PlaceOrderView.as_view(), name='place_order'),
#     path('register/', RegistrationAPIView.as_view(), name='register'),
#     path('login/', LoginAPIView.as_view(), name='login'), 
#     path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
#     path('send-otp/',views.send_otp),
#     path('verify-otp/',views.verify_otp,name="verify-otp"),
#     path('about-us/',views.about_us,name="about-us"),
#     path('login-signup/',views.login_signup,name="login-signup"),
#     path('contact-us/',views.contact_us,name="contact-us"),
#     path('services',ServicesAPIView.as_view(),name='service'),
#     # path('get_services/', get_services, name='get_services'),
#     path('submit_order/', submit_order, name='submit_order'),
#     path('book-now/', book_orders, name='book-now'),
#     path('profile/', profile, name='profile'),
#     path('api/token/refresh/',YourProtectedView.as_view(), name='token_refresh'),
#     path('update_profile/', update_profile, name='update_profile'),
# ]  
 
from django.urls import path, include  # Add include
from .views import CreateOrderViewSet, OrderPatchView, RatingViewSet, RelatedDocumentViewSet, VolunteerProfileViewSet, index, PlaceOrderView, about_us, update_profile, ServicesViewSet, upload_document
from . import views
from .views import RegistrationAPIView,OrderViewSet,ActiveOrderViewSet, LoginAPIView, UserProfileViewSet, ServicesAPIView, submit_order, book_orders, YourProtectedView
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Swarn Sarthi '                  
admin.site.index_title = 'Swarn Sarthi administration'                 
admin.site.site_title = 'Swarn Sarthi Admin Panel'

router = DefaultRouter()
router.register(r'services', ServicesViewSet)
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'active-orders', ActiveOrderViewSet, basename='active-orders')
router.register(r'create-orders', CreateOrderViewSet, basename='create-orders')
router.register(r'related-documents', RelatedDocumentViewSet,basename='related-documents')
router.register(r'ratings', RatingViewSet,basename='ratings')
router.register(r'volunteer-profiles', VolunteerProfileViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'), 
    # path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('send-otp/', views.send_otp),
    path('verify-otp/', views.verify_otp, name="verify-otp"),
    path('about-us/', views.about_us, name="about-us"),
    path('login-signup/', views.login_signup, name="login-signup"),
    path('contact-us/', views.contact_us, name="contact-us"),
    # path('services/', include(router.urls)),  # Include router URLs
    path('submit_order/', submit_order, name='submit_order'),
    path('book-now/', book_orders, name='book-now'),
    # path('profile/', profile, name='profile'),
    path('api/', include(router.urls)),
    path('api/token/refresh/', YourProtectedView.as_view(), name='token_refresh'),
    path('update_profile/', update_profile, name='update_profile'),
    path('accept-orders/<int:pk>/', OrderPatchView.as_view(), name='order-patch'),
    path('api/orders/<int:order_id>/upload-document/', upload_document),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)