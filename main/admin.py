from django.contrib import admin
from .models import CustomUser, RelatedDocument, Service, ElderlyProfile, VolunteerProfile, Order, Rating, Invoice, ActiveOrder, Feedback, VolunteerService

# Register the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_no', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('role', 'is_active', 'is_staff')
    ordering = ('email',)

# Register the Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'amount', 'created_at')
    search_fields = ('title',)
    ordering = ('created_at',)

# Register the ElderlyProfile model
@admin.register(ElderlyProfile)
class ElderlyProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

class VolunteerServiceInline(admin.TabularInline):
    model = VolunteerService

@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    filter_horizontal = ('selected_services',)
    inlines = [VolunteerServiceInline]


# Register the Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'elderly', 'volunteer', 'service', 'amount', 'status', 'order_date', 'completed_at')
    ordering = ('-order_date',)  # Use '-order_date' for descending order, remove the '-' if you want ascending order

admin.site.register(Order, OrderAdmin)

# Register the Rating model
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('order', 'value')

# Register the Invoice model
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount')

# Register the ActiveOrder model
@admin.register(ActiveOrder)
class ActiveOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'volunteer', 'service')
    search_fields = ('order__id', 'volunteer__user__email')
    ordering = ('order__created_at',)

# Register the ContactFormSubmission model
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('created_at',)


@admin.register(RelatedDocument)
class RelatedDocumentAdmin(admin.ModelAdmin):
    list_display = ['order', 'document']
    search_fields = ['order__invoice_no']
    list_filter = ['order__status']