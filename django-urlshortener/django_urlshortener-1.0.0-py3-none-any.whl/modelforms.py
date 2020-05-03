from django import forms
from django.forms import ModelForm
from urlshortener.models import URLShortenerModel


class URLShortenerModelForm(ModelForm):
    class Meta:
        model   = URLShortenerModel
        fields  = ["url"]
        widgets = {
            "url": forms.URLInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Shorten your link.'})
        }
