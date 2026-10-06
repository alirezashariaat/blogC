from django.contrib import admin
from .models import Post,Comment

# Register your models here.
admin.sites.AdminSite.site_header = "پنل مدریت"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    date_hierarchy = 'published_at'
    list_editable = ['status']
    list_display_links = ['created_at', 'title']
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','created_at','post','active']
    list_filter = ['created_at']
    date_hierarchy = 'updated_at'
    list_editable = ['active']
    list_display_links = ['first_name','last_name','created_at','post']
    