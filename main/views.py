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
from .serializers import CustomUserSerializer, ElderlyProfileSerializer, OrderSerializer, RatingSerializer, RelatedDocumentSerializer, UserProfileSerializer ,UserProfileUpdateSerializer, VolunteerProfileRatingSerializer
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
from rest_framework import viewsets
from .serializers import ServiceSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
import base64
from django.core.files.base import ContentFile
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import FileUploadParser

def send_otp_email(email, otp):
    print("5")
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = settings.EMAIL_HOST_USER  # Replace with your Gmail email address
    print("test",subject,message,from_email,[email])
    send_mail(subject, message, from_email, [email])

@csrf_exempt
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
                # Return OTP to frontend along with success message
                return JsonResponse({'message': 'OTP sent successfully!', 'otp': otp})
            else:
                return JsonResponse({'error_message': 'Email not provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error_message': 'Invalid JSON in request body'}, status=400)

    return JsonResponse({'error_message': 'Invalid request'}, status=400)



@csrf_exempt
def verify_otp(request):
    print("debug",request.body)
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        user_input_otp = body_data.get('otp')
        # user_input_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        print("otp",user_input_otp)
        print("here",stored_otp)
        print(request.session.keys())
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
            
            if CustomUser.objects.filter(email=email).exists():
                return Response({'detail': 'Email is already registered. Login to continue.'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the user
            user = serializer.save()

            # Create profile based on role
            if user.role == 'volunteer':
                VolunteerProfile.objects.create(user=user)
            elif user.role == 'elderly':
                ElderlyProfile.objects.create(user=user)

            return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        print("here",request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        user_model = get_user_model()
        print("1",user_model)
        customuser = user_model.objects.filter(email=email)
        print("2")
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


# class UserProfileUpdateView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def put(self, request):
#         user = request.user
#         print("d",request.data)
#         serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
class UserProfileUpdateViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileUpdateSerializer

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_user_profile(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

from django.shortcuts import render, redirect
from .models import ElderlyProfile, Order, Rating, RelatedDocument, Service , Feedback , CustomUser , ActiveOrder, VolunteerProfile

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


# def profile(request):
#     user = request.user
#     user_serializer = CustomUserSerializer(user)

#     # Retrieve user's orders
#     orders = Order.objects.filter(elderly__user=user)
#     orders_serializer = OrderSerializer(orders, many=True)
#     print("h")
#     context = {
#         'user_data': user_serializer.data,
#         'orders_data': json.dumps(orders_serializer.data),
#     }
#     return render(request, 'profile.html', context)
User = get_user_model()


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        print("U",request.data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Save the updated fields
        serializer.save()

        return Response(serializer.data)
    
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

# @require_GET
# def get_services(request):
#     services = Service.objects.values('id', 'title','amount')
#     return JsonResponse(list(services), safe=False)

class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    # Override the list method to customize the response
    def list(self, request, *args, **kwargs):
        services = self.get_queryset()
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)

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


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'volunteer':
                volunteer_profile = VolunteerProfile.objects.get(user=user)
                queryset = Order.objects.filter(volunteer=volunteer_profile)
            elif user.role == 'elderly':
                queryset = Order.objects.filter(elderly__user=user)
            else:
                # If the user has no specific role, return an empty queryset
                queryset = Order.objects.none()
            print("Filtered queryset count:", queryset.count())
            print("Filtered queryset:", queryset)
            print("User email:", user.email)
            return queryset
        else:
            print("User is not authenticated.") 
            return Order.objects.none() 

        
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        print("Retrieved object:", obj)
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                print("Authenticated user:", user)
                print("Partial update request data:", request.data)
                queryset = self.get_queryset()  # Debug: Print queryset before filtering
                instance = self.get_object()  # Debug: Print retrieved object
                print("Partial update instance:", instance)
                current_status = instance.status
                print("Current status:", current_status)
                order_status = request.data.get('status')
                print("Received order status:", order_status)

                # Assign user to volunteer field
                volunteer_profile = VolunteerProfile.objects.get(user=user)
                instance.volunteer = volunteer_profile

                if order_status:
                    instance.status = order_status
                else:
                    return Response({"detail": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)

                instance.save()
                print("Order updated successfully.")
                return Response({"detail": "Order updated successfully"}, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                print("Order does not exist.")
                return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
            except VolunteerProfile.DoesNotExist:
                print("Volunteer profile does not exist.")
                return Response({"detail": "Volunteer profile not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print("Error:", e)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Authentication credentials were not provided.")
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework import serializers

class ActiveOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    service = ServiceSerializer()
    elderly = ElderlyProfileSerializer()
    class Meta:
        model = ActiveOrder
        fields = ['id', 'order', 'volunteer', 'service', 'elderly']
        read_only_fields = ['id', 'order', 'volunteer', 'service', 'elderly']
class ActiveOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(volunteer=None)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "Not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class OrderPatchSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=20, required=True)


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['service', 'amount', 'status', 'order_date', 'completed_at', 'invoice_no', 'related_documents']
        
from django.contrib import messages
from rest_framework import permissions
HTTP_450_BLOCKED = 450  # Define a custom status code

class CustomStatusCodes:
    HTTP_450_BLOCKED = 450 

class IsProfileComplete(permissions.BasePermission):
    message = 'Please complete your profile before making a booking.'

    def has_permission(self, request, view):
        try:
            custom_user = CustomUser.objects.get(pk=request.user.pk)
        except CustomUser.DoesNotExist:
            return False

        required_fields = ['first_name', 'last_name', 'phone_no', 'address', 'state', 'country']
        if all(getattr(custom_user, field) for field in required_fields):
            return True
        else:
            # Return a custom response with status code 450
            return Response({'detail': self.message}, status=HTTP_450_BLOCKED)

    

class CreateOrderViewSet(viewsets.GenericViewSet):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Fetch the elderly user from the request
            elderly_user = request.user

            # Check if the user's profile is complete
            if not IsProfileComplete().has_permission(request, self):
                return Response({'detail': 'Please complete your profile before making a booking.'}, status=HTTP_450_BLOCKED)

            # Fetch the ElderlyProfile associated with the user
            try:
                elderly_profile = elderly_user.elderly_profile
            except ElderlyProfile.DoesNotExist:
                return Response({'detail': 'Elderly profile not found.'}, status=status.HTTP_400_BAD_REQUEST)

            # Assign the elderly_profile to the elderly field
            serializer.validated_data['elderly'] = elderly_profile

            # Call the super create method to save the order
            serializer.save()

            # Return the created order
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class OrderPatchView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderPatchSerializer
    permission_classes = [IsAuthenticated, IsProfileComplete]
    
    def update(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'volunteer':
            order = self.get_object()
            serializer = self.get_serializer(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            # Check if the user's profile is complete
            required_fields = ['first_name', 'last_name', 'phone_no', 'address', 'state', 'country']
            if not all(getattr(user, field) for field in required_fields):
                return Response({'detail': 'Please complete your profile before updating the order.'}, status=HTTP_450_BLOCKED)
            # Update the order
            order.volunteer = user.volunteer_profile
            order.status = serializer.validated_data['status']
            order.save()

            return Response({'detail': 'Order updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def upload_document(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        file_obj = request.FILES.get('file')
        document = RelatedDocument.objects.create(order=order, document=file_obj)
        serializer = RelatedDocumentSerializer(document)
        return Response(serializer.data, status=201)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

class RelatedDocumentViewSet(viewsets.ModelViewSet):
    queryset = RelatedDocument.objects.all()
    serializer_class = RelatedDocumentSerializer

class VolunteerProfileViewSet(viewsets.ModelViewSet):
    queryset = VolunteerProfile.objects.all()
    serializer_class = VolunteerProfileRatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
    
    def partial_update(self, request):
        # Get the volunteer profile associated with the request user
        volunteer_profile = VolunteerProfile.objects.get(user=request.user)

        # Get the rating data from the request payload
        rating_data = request.data.get('rating_data')  # Assuming the rating data is sent along with the request

        # Update the volunteer profile with the received rating
        serializer = VolunteerProfileRatingSerializer(volunteer_profile, data=rating_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()