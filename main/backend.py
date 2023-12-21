from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            print("aya?",email,self,request)
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None 

        if user.check_password(password):
            print("user",user)
            return user 
        return None
 