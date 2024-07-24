from django import forms
from django.contrib.auth.models import User
from .models import Author, Title, Country
import re

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
        
class ORCIDField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return ''
        
        # Remove any existing dashes from the input value
        value = value.replace('-', '')
        
        # Insert dashes every 4 characters if not already present
        formatted_value = '-'.join(value[i:i+4] for i in range(0, len(value), 4))
        return formatted_value

    def validate_orcid(self, value):
        # Validate the ORCID format with alphabets, digits, and dashes
        if not re.match(r'^[A-Za-z\d-]*$', value):
            raise forms.ValidationError('Invalid ORCID format. Use alphabets, digits, and dashes only.')
        return value


class UserRegistrationForm(forms.ModelForm):
    title = forms.ModelChoiceField(
        queryset=Title.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control custom-select'}),
        label='Title'
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
        label='First Name'
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
        label='Last Name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}),
        label='Enter Email'
    )
    institution = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Institution'}),
        label='Institution / Affiliation'
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'rows': 10}),
        label='Address'
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        label='City'
    )
    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your State'}),
        label='State'
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control custom-select'}),
        label='Country'
    )
    mobile_no = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        label='Mobile Number'
    )
    zipcode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Pincode'}),
        label='Zipcode'
    )
    orcid_id = ORCIDField(
        max_length=19,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ORCID ID (e.g., XXXX-XXXX-XXXX-XXXX)'}),
        label='ORCID ID'
    )
    scopus_id = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'scopusid'}),
        label='Scopus id'
    )

    class Meta:
        model = User
        fields = ('title', 'first_name', 'last_name', 'email', 'institution', 'address', 'city', 'state', 'country', 'mobile_no', 'zipcode', 'orcid_id', 'scopus_id')

    def clean_orcid_id(self):
        orcid_id = self.cleaned_data.get('orcid_id')
        return self.fields['orcid_id'].validate_orcid(orcid_id)


    