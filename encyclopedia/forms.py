from django import forms
from django.utils.safestring import mark_safe

class PageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=30)
    content = forms.CharField(label="Content", widget=forms.Textarea)

class EditForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)