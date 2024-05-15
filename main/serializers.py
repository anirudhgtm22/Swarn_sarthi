# serializers.py
from rest_framework import serializers
from .models import CustomUser, ElderlyProfile , Order, Rating, RelatedDocument, Service , VolunteerProfile
from django.contrib.auth.hashers import make_password
# class CustomUserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
 
#     class Meta:
#         model = CustomUser  
#         # fields = ('id', 'email', 'first_name', 'last_name', 'role', 'password')
#         fields = '__all__'
        
#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             email=validated_data['email'],
#             first_name=validated_data['first_name'], 
#             last_name=validated_data['last_name'],
#             role=validated_data['role'],  
#             password=validated_data['password'], 
#             phone_no = '',
#             profile_picture = '', 
#         ) 
#         print('c')
#         return user
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser  
        fields = ['id','email', 'password','first_name', 'last_name', 'role','profile_picture']
    
    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

class CustomUserOrderSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser  
        fields = '__all__'

    def create(self, validated_data):
        print("VD",validated_data)
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=password,
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            role = validated_data['role'],
        )
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_no')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ElderlyProfileSerializer(serializers.ModelSerializer):
    user = CustomUserOrderSerializer()
    class Meta:
        model = ElderlyProfile
        fields = '__all__'

class VolunteerProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = VolunteerProfile  
        fields = '__all__'    

class RelatedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedDocument
        fields = '__all__'     

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['order', 'value', 'feedback']

class OrderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()  # Include this line to serialize the 'service' field
    elderly = ElderlyProfileSerializer()
    volunteer = VolunteerProfileSerializer()
    rating = RatingSerializer()
    class Meta:
        model = Order
        fields = '__all__'

class ServicesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Service
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser  
        fields = '__all__'


        
class VolunteerProfileRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerProfile
        fields = ['user', 'rating']