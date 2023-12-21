# serializers.py
from rest_framework import serializers
from .models import CustomUser, ElderlyProfile , Order, Service , VolunteerProfile

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
 
    class Meta:
        model = CustomUser  
        # fields = ('id', 'email', 'first_name', 'last_name', 'role', 'password')
        fields = '__all__'
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name'],
            role=validated_data['role'],  
            password=validated_data['password'], 
            phone_no = '',
            profile_picture = '', 
        ) 
        print('c')
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
    user = CustomUserSerializer()
    class Meta:
        model = ElderlyProfile
        fields = '__all__'

class VolunteerProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = VolunteerProfile  
        fields = '__all__'    
        
class OrderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()  # Include this line to serialize the 'service' field
    elderly = ElderlyProfileSerializer()
    volunteer = VolunteerProfileSerializer()
    class Meta:
        model = Order
        fields = '__all__'