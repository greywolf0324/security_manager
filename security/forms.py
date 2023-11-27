from django import forms
from django.core.validators import FileExtensionValidator
from .models import ProcessHistory

class ProcessForm(forms.Form):
  data = forms.FileField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}), validators=[FileExtensionValidator(['pdf', 'xlsx', 'xls'])])
  additions = forms.CharField(widget=forms.Textarea)
  input = forms.CharField(widget=forms.Textarea)
  customername = forms.CharField(max_length=255)
  currency = forms.CharField(max_length=10)

# class HistoryForm(forms.Form):

