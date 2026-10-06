from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        Model = Comment
        fields = ['first_name', 'last_name',
                  'content',]
        widgets = {
            'first_name':forms.TextInput(), 'last_name':forms.TextInput(),
                  'content':forms.Textarea(),
        }
