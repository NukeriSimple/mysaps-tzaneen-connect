from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Case, IncidentCategory

class CaseReportForm(forms.ModelForm):
    """Case reporting form with bilingual support"""
    
    class Meta:
        model = Case
        fields = ('category', 'title', 'description', 'title_ts', 'description_ts',
                  'location_description', 'location_description_ts', 
                  'contact_name', 'contact_phone', 'contact_email')
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5, 
                'placeholder': 'Describe what happened in English...'
            }),
            'description_ts': forms.Textarea(attrs={
                'rows': 5, 
                'placeholder': 'Hlamusela leswi endleke hi Xitsonga...',
                'class': 'form-control'
            }),
            'title_ts': forms.TextInput(attrs={
                'placeholder': 'Xihoko hi Xitsonga (optional)'
            }),
            'location_description': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'e.g., Near Tzaneen Mall, next to the taxi rank...'
            }),
            'location_description_ts': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Xikombiso: Kusuhi na Tzaneen Mall, eka taxi rank...',
                'class': 'form-control'
            }),
            'contact_name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'contact_phone': forms.TextInput(attrs={'placeholder': 'Cellphone number for updates'}),
            'contact_email': forms.EmailInput(attrs={'placeholder': 'Email (optional)'}),
        }
        labels = {
            'title': 'Case Title (English)',
            'title_ts': 'Case Title (Xitsonga) - Optional',
            'description': 'Description (English)',
            'description_ts': 'Description (Xitsonga) - Optional',
            'location_description': 'Location (English)',
            'location_description_ts': 'Location (Xitsonga) - Optional',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['contact_name'].initial = self.user.get_full_name() or self.user.username
            self.fields['contact_phone'].initial = self.user.phone_number
            self.fields['contact_email'].initial = self.user.email
        
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs.update({'class': 'form-control'})