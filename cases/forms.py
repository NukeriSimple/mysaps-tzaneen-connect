from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Case, IncidentCategory

class CaseReportForm(forms.ModelForm):
    """Case reporting form"""
    
    class Meta:
        model = Case
        fields = ('category', 'title', 'description', 'location_description', 
                  'contact_name', 'contact_phone', 'contact_email')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': _('Describe what happened...')}),
            'location_description': forms.Textarea(attrs={'rows': 3, 'placeholder': _('e.g., Near Tzaneen Mall, next to the taxi rank...')}),
            'contact_name': forms.TextInput(attrs={'placeholder': _('Your name')}),
            'contact_phone': forms.TextInput(attrs={'placeholder': _('Cellphone number for updates')}),
            'contact_email': forms.EmailInput(attrs={'placeholder': _('Email (optional)')}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['contact_name'].initial = self.user.get_full_name() or self.user.username
            self.fields['contact_phone'].initial = self.user.phone_number
            self.fields['contact_email'].initial = self.user.email
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})