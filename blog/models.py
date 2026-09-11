from django.db import models
from django.contrib.auth.models import User

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
    title = models.CharField(max_length = 150,verbose_name='عنوان')
    content = models.TextField(verbose_name='محتوا')
    slug = models.SlugField(max_length = 200, verbose_name = 'اسلاگ')
    status = models.CharField(max_length = 3, choices=Status.choices ,default=Status.DRAFT, verbose_name='وضعیت انتشار')
    # Date related
    created_at = models.DateTimeField(auto_now_add = True)
    published_at = models.DateTimeField(blank = True,null = True)
    updated_at = models.DateTimeField(auto_now = True)

    author = models.ForeignKey(User, on_delete = models.CASCADE,related_name = 'posts')

    def __str__(self):
        return f"{self.title}"
    class Meta:
        ordering = ['-published_at']
        indexes = [models.Index(fields=['title', 'published_at'])]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'






