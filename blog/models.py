from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

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
                            blank=True, verbose_name='اسلاگ')
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(
        default=False, verbose_name='نمایش / عدم نمایش')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'
        indexes = [models.Index(fields=['first_name', 'created_at'])]
