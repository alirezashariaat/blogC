from django.contrib import admin
from .models import Ticket

# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    date_hierarchy = 'created_at'
    list_display_links = ['created_at', 'subject']
