from . import views
from django.urls import path
app_name = "ticket"
urlpatterns = [
    path("", views.ticket, name="ticket"),
]
