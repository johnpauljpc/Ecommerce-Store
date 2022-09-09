from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES =(
	('S', 'Stripe'),
	('P', 'Paypal')
	)
class CheckoutForm(forms.Form):
	street_address = forms.CharField(widget = forms.TextInput(attrs={
		'class': "form-control",
		'placeholder':'Mainland street'
		}))
	appartment_address = forms.CharField(required = False, widget=forms.TextInput(attrs={
		'class': "form-control",
		'placeholder':'second apartment'
		}))
	country = CountryField(blank_label='(select country)').formfield(widget = CountrySelectWidget(attrs={
		'class':"custom-select d-block w-100"
		}))
	zipcode = forms.IntegerField(widget = forms.TextInput(attrs={
		'class':"form-control"
		}))
	same_billing_address = forms.BooleanField(required = False, widget = forms.CheckboxInput())
	save_info = forms.BooleanField (required = False, widget = forms.CheckboxInput())
	payment_option = forms.ChoiceField(widget = forms.RadioSelect, choices = PAYMENT_CHOICES)
	#payment_option = forms.BooleanField(widget = forms.RadioSelect(choices = PAYMENT_CHOICES))
	
