from django import forms
from .models import Dashboard


class UploadFileForm(forms.Form):
    file = forms.FileField()
    dashboard = forms.ModelChoiceField(
        queryset=Dashboard.objects.all(), label="Choose an existing Dashboard"
    )
