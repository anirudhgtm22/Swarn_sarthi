# views.py
from django.contrib.auth import authenticate,login,logout
import random ,json
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse , get_object_or_404
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer, OrderSerializer ,UserProfileUpdateSerializer
from django.http import HttpResponse, JsonResponse
from django.views import View
from .utils import generate_invoice, send_invoice_email
from rest_framework.permissions import IsAuthenticated
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET, require_POST
import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.http import require_http_methods

def send_otp_email(email, otp):
    print("5")
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = settings.EMAIL_HOST_USER  # Replace with your Gmail email address
    print("test",subject,message,from_email,[email])
    send_mail(subject, message, from_email, [email])


def send_otp(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            email = body_data.get('email')
            if email:
                # Generate OTP dynamically
                otp = str(random.randint(1000, 9999)) 
                # Send OTP via email
                send_otp_email(email, otp)
                # Store OTP in session for verification
                request.session['otp'] = otp

                return JsonResponse({'message': 'OTP sent successfully!'})
            else:
                return JsonResponse({'error_message': 'Email not provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error_message': 'Invalid JSON in request body'}, status=400)

    return JsonResponse({'error_message': 'Invalid request'}, status=400)


def verify_otp(request):
    print("debug")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        user_input_otp = body_data.get('otp')
        # user_input_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if user_input_otp == stored_otp: 
            return JsonResponse({'message': 'Success!'})
        else:
            return JsonResponse({'error_message': 'Incorrect OTP. Please try again.'}, status=400)
    
    return JsonResponse({'error_message': 'Invalid request'}, status=400)

def index(request):
    print("ka",request)
    is_authenticated = request.user.is_authenticated
    return render(request, 'index.html', {'is_authenticated': is_authenticated}) 


def about_us(request):
    return render(request,'about.html')

class ServicesAPIView(APIView):
    def render_services_template(self, request):
        active_orders = Order.objects.filter(status='created')
        serializer = OrderSerializer(active_orders, many=True)
        serialized_data = serializer.data
        for order_data in serialized_data:
            order_id = order_data.get('id')
            amount = order_data.get('amount')
            status = order_data.get('status')
            created_at = order_data.get('created_at')
            service_data = order_data.get('service', {})
            service_name = service_data.get('title')  # Adjust this according to your Service model fields
            
        context = {
            'orders': serialized_data,
        }
        return render(request, 'services.html', context)

    def get(self, request, *args, **kwargs):
        return self.render_services_template(request)

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, *args, **kwargs):
        print("hiiii", request.data)
        # Extract data from the request
        email = request.data.get('email')
        order_id = request.data.get('order_id')
        
        
        # Fetch the order from the database
        try:
            order = Order.objects.get(id=order_id)
            
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the VolunteerProfile instance
        volunteer_profile = get_object_or_404(VolunteerProfile, user__email=email)
        print("email",volunteer_profile)
        # Update the 'volunteer' field with the provided VolunteerProfile instance
        order.volunteer = volunteer_profile
        order.status = 'volunteer_assigned'
        order.save()
        print(order)
        # Render the service.html page
        return Response({'status': 'success', 'message': 'Service accepted successfully'}, status=status.HTTP_200_OK)

def contact_us(request):  
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message') 

        # Save data to the model
        Feedback.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            message=message
        )

        return JsonResponse({'message': 'Thanks! We will get in touch with you shortly.'})
    
    return render(request, 'contactUs.html')

def login_signup(request):
    return render(request,'login-signup.html')



class PlaceOrderView(View):
    print("di")
    def post(self, request, *args, **kwargs):
        print("1")
        # Your order processing logic here...

        # Assume you have order details available
        order_details = {
            'order_id': '12345',
            'total_amount': 100.0,
            # Add more order details as needed
        }
        email = 'smartboyanirudh@gmail.com'
        print("ew")
        # Generate invoice PDF
        invoice_pdf_path = f'media/invoices/invoice_{order_details["order_id"]}.pdf'
        print("dfw")
        generate_invoice(order_details, invoice_pdf_path)
        print("df")

        # Send invoice via email
        send_invoice_email(email, invoice_pdf_path)
        print("d")
        return HttpResponse("Order placed successfully!")
    
class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if the email already exists
            if CustomUser.objects.filter(email=email).exists():
                return Response({'detail': 'Email is already registered. Login to continue.'}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        user_model = get_user_model()
        print("1",user_model)
        customuser = user_model.objects.filter(email=email)
        if user:
            # Log in the user 
            login(request, user)
            # Generate JWT tokens 
            print("de",customuser)
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'is_authenticated': True,
                'email': email,
                'role': user.role,
                'user': {
                    'user': user.first_name,
    
                }
            }
            
            return JsonResponse(response_data)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        print("d",request.data)
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
    

from django.shortcuts import render, redirect
from .models import ElderlyProfile, Order, Service , Feedback , CustomUser , ActiveOrder, VolunteerProfile

def create_order(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = Service.objects.get(pk=service_id)

        # Create a new order with the associated service
        order = Order.objects.create(
            elderly=request.user.elderly_profile,  # Assuming you have a related name for the elderly profile
            service=service
        )
        order.save()

        return redirect('order_success')  # Redirect to a success page or wherever you want

    # Retrieve services to display in the form
    services = Service.objects.all()
    return render(request, 'create_order.html', {'services': services})

User = get_user_model()


def profile(request):
    user = request.user
    user_serializer = CustomUserSerializer(user)

    # Retrieve user's orders
    orders = Order.objects.filter(elderly__user=user)
    orders_serializer = OrderSerializer(orders, many=True)
    print("h")
    context = {
        'user_data': user_serializer.data,
        'orders_data': json.dumps(orders_serializer.data),
    }
    return render(request, 'profile.html', context)

class YourProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        # Get the refresh token from the request data
        print("hi")
        user = request.user
        print("user",user)
        # Retrieve user details as needed
        user_details = {
            'user_id': user.id,
            'email': user.email,
            # Add more user details as needed
        }
        print("ud",user_details)
        # Render the profile.html template with user details
        # return render(request, 'profile.html', {'user_details': user_details})
        return Response(user_details)

@require_GET
def get_services(request):
    services = Service.objects.values('id', 'title','amount')
    return JsonResponse(list(services), safe=False)

@require_POST
def submit_order(request):
    # Extract form data from the request
    data = request.POST
    service_id = data.get('service')
    amount = data.get('amount')
    order_date = data.get('date') + ' ' + data.get('time')  # Concatenate date and time
    email = data.get('email')
    order_id = data.get('orderId')
    order_title = data.get('orderTitle')
    print("data",data)

    # Find the user based on email
    user = User.objects.get(email=email)
    print("user",user)
    # Find the ElderlyProfile based on the user's first name
    elderly_profile = ElderlyProfile.objects.get(user=user)
    print("e",elderly_profile)
    service = Service.objects.get(title=order_title)
    
    print("s",service)
    # Create a new order
    order = Order.objects.create(
        elderly=elderly_profile,  # Replace with the actual ElderlyProfile ID
        volunteer_id=None,  # Replace with the actual VolunteerProfile ID if available
        service=service,
        amount=amount,
        status='created', # Use UUID for invoice number
    )
    print("order",order)
    return JsonResponse({'message': 'Order submitted successfully'})

def book_orders(request):
    # Fetch all services from the database
    services = Service.objects.all()
    # Pass the services to the template as context data
    context = {'services': services}
    
    return render(request, 'orders.html', context)

from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs


@login_required
@require_http_methods(["PUT"])
def update_profile(request):
    user = request.user
    print("Request body:", request)
    # Decode the request body to a string
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print("f",body)
    # Extract data from the JSON object
    first_name = body.get('first_name')
    last_name = body.get('last_name')
    phone_no = body.get('phone_no')
    address = body.get('address')
    email = body.get('email')
    role = body.get('role')
    country = body.get('country')
    state = body.get('state')
    full_address = f"{address}, {state}, {country}"
    # Update user model fields
    user.first_name = first_name
    user.last_name = last_name
    user.phone_no = phone_no
    user.address = address
    user.country = country
    user.state = state

    # Save the updated user
    user.save()
    return JsonResponse({'status': 'success'})    