from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from .models import Customer, Contact

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget= forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget= forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}))
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autofocus':True, "autocomplete": "email", 'class': 'form-control'}),
    )

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autofocus':True, "autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )

class CustomerProfileForm(UserChangeForm):
    username = forms.CharField(label=_("Username"), strip=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label=_("First Name"), strip=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_("Last Name"), strip=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=_("Email"),  widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        

class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['shipping_address', 'phone']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows':4}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['cname', 'phone', 'email', 'message']
        labels = {
            'cname': 'Name',
        }
        widgets = {
            'cname': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'How can we help you?', 'style':'height:150px;'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=200)