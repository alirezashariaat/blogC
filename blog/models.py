from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import os
import re
from PIL import Image as ImagePackage
from django_resized import ResizedImageField
# Managers


class AcceptedPost(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.ACCEPTED)


class Post(models.Model):
    """
    This class manages the fields of post DB
    """

    class Status(models.TextChoices):
        """
        This class manages the situation(status) of post
        """
        DRAFT = ('DF', 'DRAFT')
        REJECTED = ('RJ', 'REJECTED')
        ACCEPTED = ('ACC', 'ACCEPTED')

    # Post context
    title = models.CharField(max_length=150, verbose_name='عنوان')
    content = models.TextField(verbose_name='محتوا')
    slug = models.SlugField(max_length=200, unique=True,
                            blank=True, verbose_name='اسلاگ', allow_unicode=True)
    status = models.CharField(max_length=3, choices=Status.choices,
                              default=Status.DRAFT, verbose_name='وضعیت انتشار')
    # Date related
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')

    objects = models.Manager()
    accepted = AcceptedPost()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    class Meta:
        ordering = ['-published_at']
        indexes = [models.Index(fields=['title', 'published_at'])]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'


class Comment(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=70, verbose_name=' نام خانوادگی')
    content = models.TextField(verbose_name='محتوا')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    reading_time = models.PositiveIntegerField(
        default=5, verbose_name='زمان مطالعه')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(
        default=False, verbose_name='نمایش / عدم نمایش')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'
        indexes = [models.Index(fields=['first_name', 'created_at'])]


def image_upload_path(instance, filename):
    today = date.today().strftime('%Y/%m/%d')
    post_title = instance.post.title
    filename_slug = slugify(post_title, allow_unicode=True)
    extension = os.path.splitext(filename)[1].lower()
    return f"post_images/{today}/{filename_slug}{extension}"


class Image(models.Model):
    image_file = ResizedImageField(
        upload_to=image_upload_path, verbose_name='تصویر', size=[1200, 900], quality=80)
    title = models.CharField(
        max_length=100, verbose_name='عنوان', blank=True, unique=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images', verbose_name='پست')
    description = models.TextField(
        verbose_name='توضیحات', blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'


# برای resize کردن دو روش میتوان استفاده کرد:
# 1. Rewrite کردن method save به صورت زیر
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     if self.image_file:
    #         with ImagePackage.open(self.image_file.path) as img:
    #             img.thumbnail((800, 600))
    #             img.save(self.image_file.path)
# 2. استفاده ار package django_resize
# from django_resized import ResizedImageField
#  image = ResizedImageField(
#         size=[1200, 900],
#         quality=80,
#         upload_to='posts/',
#         blank=True,
#         null=True,
#     )
