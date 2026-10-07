from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['first_name',
                  'last_name',
                  'content',]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'دیدگاه شما'}),
        }
