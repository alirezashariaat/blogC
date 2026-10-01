from django.db import models
from django.core.exceptions import ValidationError


class Ticket(models.Model):
    class Status(models.TextChoices):
        RESPONDED = ('RP', 'RESPONDED')
        UNRESPONDED = ('URP', 'UNRESPONDED')
    message = models.TextField(verbose_name='متن تیکت')
    first_name = models.CharField(
        max_length=50, verbose_name='نام', null=True, blank=True)
    last_name = models.CharField(
        max_length=70, verbose_name='نام خانوادگی', null=True, blank=True)
    email = models.EmailField(verbose_name='ایمیل', blank=True, null=True)
    phone = models.CharField(
        max_length=11, verbose_name='تلفن', blank=True, null=True)
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    response = models.TextField(verbose_name='پاسخ', blank=True, null=True)
    status = models.CharField(max_length=3,
                              choices=Status.choices, default=Status.UNRESPONDED, verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.email and not self.phone:
            raise ValidationError(
                "لطفا یکی از فیلد های تلفن یا ایمیل را پر کنید")

    def save(self, *args, **kwargs):
        if self.response and self.response.strip():
            self.status = self.Status.RESPONDED
        else:
            self.status = self.Status.UNRESPONDED

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        ordering = ['created_at']
        indexes = [models.Index(fields=['subject', 'created_at'])]
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'
