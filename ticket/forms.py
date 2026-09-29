from importlib.metadata import requires

from django import forms

from .models import Ticket
class TicketForm(forms.ModelForm):
    SUBJECT_CHOICES = (('suggestin','پیشنهاد'))
    message = forms.TextField(widget = forms.Textarea,required = True)
    first_name = forms.CharField(widget = forms.CharField,max_length=50 ,required = True)
    last_name = forms.CharField(widget = forms.CharField,max_length=70 ,required = True)
    email = forms.EmailField()
    phone = forms.CharField()
    subject = forms.CharField(widget=  forms.CharField,max_length=100, required = True)
    class Meta:
        model = Ticket
        fields = ['first_name','last_name','email','phone','subject']