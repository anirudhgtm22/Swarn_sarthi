# models.py
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from .utils import generate_invoice_number
from datetime import datetime

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, role, phone_no=None, password=None, **extra_fields):
#         print("hi")
#         email = self.normalize_email(email)
#         user = self.model(email=email, first_name=first_name, last_name=last_name, phone_no=phone_no, role=role, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         if role == 'volunteer': 
#             VolunteerProfile.objects.create(user=user)
#         elif role == 'elderly':
#             ElderlyProfile.objects.create(user=user)
#         return user

#     def create_superuser(self, email, first_name, last_name,role, phone_no, profile_picture, password=None, **extra_fields):
#             extra_fields.setdefault('is_staff', True)
#             extra_fields.setdefault('is_superuser', True)  # Add this line to set the role explicitly
#             return self.create_user(email, first_name, last_name,role, phone_no, profile_picture, password, **extra_fields)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_no, profile_picture, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, phone_no, profile_picture, role, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    role = models.CharField(max_length=20, null=True, blank=True, choices=[('volunteer', 'Volunteer'), ('elderly', 'Elderly'), ('admin', 'Admin')])

    address = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_no', 'role']

    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='customuser_set', related_query_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='customuser_set', related_query_name='user_permissions')

    @property
    def full_address(self):
        return f"{self.address}, {self.state}, {self.country}"

    def __str__(self):
        return self.email



class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True,blank=True, upload_to='service/')
    def __str__(self):
        return self.title

class ElderlyProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='elderly_profile')

    def __str__(self):
        return str(self.user.email)

class VolunteerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='volunteer_profile')
    rating = models.IntegerField(default=0)
    selected_services = models.ManyToManyField(Service, blank=True, related_name='volunteers')

    def __str__(self):
        return f"Volunteer: {self.user.email} - Rating: {self.rating}"
    

class Order(models.Model):
    elderly = models.ForeignKey(ElderlyProfile, on_delete=models.CASCADE, related_name='orders')
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='volunteer_orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('created', 'Created'),
        ('volunteer_assigned', 'Volunteer Assigned'),
        ('completed', 'Completed')
    ], default='created')
    order_date = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    invoice_no = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    orderDate = models.DateTimeField(default=datetime.now) 
    related_documents = models.ManyToManyField('RelatedDocument', blank=True, related_name='orders')  # Updated related_name

    def __str__(self):
        return f"Order {self.invoice_no} - Status: {self.status}"

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.service.amount
        if not self.invoice_no:
            self.invoice_no = generate_invoice_number()
        super().save(*args, **kwargs)

class RelatedDocument(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='order_documents/')

    def __str__(self):
        return f"Related Document for Order {self.order.invoice_no}"

    
@receiver(post_save, sender=Order)
def create_active_order(sender, instance, created, **kwargs):
    if created and instance.status == 'created':
        ActiveOrder.objects.create(order=instance, volunteer=instance.volunteer, service=instance.service , elderly = instance.elderly)

@receiver(post_save, sender=Order)
def update_invoice(sender, instance, **kwargs):
    if instance.status == 'completed':
        # Check if the order already has an associated invoice
        existing_invoice = Invoice.objects.filter(order=instance).first()

        if existing_invoice is None:
            # If no existing invoice, create a new one
            invoice = Invoice(order=instance)

            # Check if the amount is provided and is greater than 0 before saving
            if instance.amount is not None and instance.amount > 0:
                invoice.amount = instance.amount
            else:
                # If amount is not provided or invalid, set a default value or handle it as needed
                invoice.amount = 0  # You can adjust this default value

            invoice.save()


@receiver(post_save, sender=Order)
def delete_active_order(sender, instance, **kwargs):
    if instance.status == 'completed':
        ActiveOrder.objects.filter(order=instance).delete()

class Rating(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='rating')
    value = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rating for Order {self.order.id} - Value: {self.value}"

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice for Order {self.order.id} - Amount: {self.amount}"

class ActiveOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='active_order')
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    elderly = models.ForeignKey(ElderlyProfile, on_delete=models.CASCADE,null=True)

    def __str__(self):
        volunteer_email = self.volunteer.user.email if self.volunteer else "None"
        return f"Active Order - Order: {self.order.id} - Service: {self.service.title} - Volunteer: {volunteer_email} - Status: {self.order.status}"

    class Meta:
        verbose_name_plural = 'Active Orders'

class Feedback(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
          
class VolunteerService(models.Model):
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='volunteer_services') 
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.volunteer.user.email} - {self.service.title} - {self.created_at}"

