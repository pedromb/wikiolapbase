from django import forms
from django.forms import ModelForm

class UploadFileForm(forms.Form):
    file = forms.FileField()