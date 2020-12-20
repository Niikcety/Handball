from django import forms
from django.core.exceptions import ValidationError

from .models import Match

class CreateForm(forms.Form):
    match_info = forms.CharField(
        widget=forms.Textarea()
    )
