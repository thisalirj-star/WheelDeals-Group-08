from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomLoginForm(AuthenticationForm):
    """Login form with Bootstrap styling."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'form-control'
        })
    )


class BuyerRegistrationForm(UserCreationForm):
    """Registration form for buyers."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'phone', 'address', 'profile_picture'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap class to auto-generated fields
        for field in ['username', 'password1', 'password2']:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'buyer'  # Force buyer type
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SellerRegistrationForm(UserCreationForm):
    """Registration form for sellers — includes company_name."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    company_name = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'company_name', 'phone', 'address', 'profile_picture'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'seller'  # Force seller type
        user.email = self.cleaned_data['email']
        user.company_name = self.cleaned_data['company_name']
        if commit:
            user.save()
        return user