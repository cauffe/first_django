from django import forms
from django.forms import ModelForm
from main.models import State, City
from django.core.validators import RegexValidator

class CitySearchForm(forms.Form):
	alphanumeric = RegexValidator(r'^[a-zA-Z\s]*$', 'Only alphanumeric characters are allowed.')
	name = forms.CharField(required=True, initial='Orem', validators=[alphanumeric])
	state = forms.CharField(required=True, initial='Utah', validators=[alphanumeric])


class CreateCityForm(forms.ModelForm):
	class Meta:
		model = City