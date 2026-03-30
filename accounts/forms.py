from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    """Simplified registration form"""
    
    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(_('This phone number is already registered.'))
        return phone

class UserProfileForm(forms.ModelForm):
    """Profile update form"""
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 
                  'preferred_language', 'notification_method', 'large_font', 
                  'voice_input', 'street_address', 'suburb', 'city', 
                  'is_business_owner', 'business_name', 'business_address')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class PhoneNumberRegistrationForm(forms.Form):
    """Phone number only registration"""
    phone_number = forms.CharField(max_length=15, label=_('Cellphone Number'))
    username = forms.CharField(max_length=150, label=_('Name'))
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(_('This phone number is already registered.'))
        return phone