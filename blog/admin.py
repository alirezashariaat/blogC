from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    date_hierarchy = 'published_at'
    list_editable = ['status']
    list_display_links = ['created_at','title']