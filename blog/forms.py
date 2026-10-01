from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=150, widget=forms.Textarea)
    content = forms.ChoiceField(widget=forms.TextInput)

    class Meta:
        model = Post
        fields = ['title', 'content']
