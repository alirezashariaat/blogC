from django.contrib import admin
from .models import Image, Post, Comment

# Register your models here.
admin.sites.AdminSite.site_header = "پنل مدیریت"


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    readonly_fields = ['first_name', 'last_name',
                       'content', 'created_at', 'updated_at']


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ['title', 'created_at']
    write_only_fields = ['image_file', 'description']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ImageInline]
    list_display = ['title', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    date_hierarchy = 'published_at'
    list_editable = ['status']
    list_display_links = ['created_at', 'title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'created_at', 'post', 'active']
    list_filter = ['created_at']
    date_hierarchy = 'updated_at'
    list_editable = ['active']
    list_display_links = ['first_name', 'last_name', 'created_at', 'post']
