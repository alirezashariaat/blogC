from django import forms
import re
from .models import Ticket


class TicketForm(forms.ModelForm):
    """
    A form for creating and updating Ticket instances.
    This form is based on the Ticket model and includes fields for first name, last name, message, email, phone, and subject. The subject field is defined as a ChoiceField with predefined options.
    """

    SUBJECT_CHOICES = (
        ('suggestion', 'پیشنهاد'),
        ('financial', 'مالی'),
        ('help', 'راهنمایی'))

    subject = forms.ChoiceField(  # بخاطر اینکه در مدل subject یک CharField است و در فرم ما میخواهیم از یک ChoiceField استفاده کنیم، باید این فیلد را دوباره تعریف کنیم
        choices=SUBJECT_CHOICES,
        required=True,
        label='موضوع'
    )

    class Meta:
        """Meta information for the TicketForm.
        Specifies the model to use and the fields to include in the form, along with custom widgets for each field.
        """

        model = Ticket
        fields = ['first_name', 'last_name',
                  'message', 'email', 'phone', 'subject']
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'phone': forms.TextInput(),

            'message': forms.Textarea(),
            'subject': forms.Select(),

        }

    def clean_phone(self):
        
        phone = self.cleaned_data.get('phone')

        if not phone:
            return phone
        elif not re.fullmatch(r'09\d{9}', phone):
            raise forms.ValidationError('شماره موبایل معتبر نیست')
