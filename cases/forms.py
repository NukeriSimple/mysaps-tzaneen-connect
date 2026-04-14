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


class CaseStatusUpdateForm(forms.ModelForm):
    """Form for admin to update case status"""
    
    class Meta:
        model = Case
        fields = ('status', 'priority', 'assigned_officer', 'assigned_officer_ts', 'assigned_station')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assigned_officer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Officer name'}),
            'assigned_officer_ts': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vito ra Ofisara (Xitsonga)'}),
            'assigned_station': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Police station / Xitlhangi'}),
        }
        labels = {
            'status': 'Case Status / Xiyimo xa Mhaka',
            'priority': 'Priority / Xiyimo xa Nkarhi',
            'assigned_officer': 'Assigned Officer / Ofisara loyi a nyikiweke',
            'assigned_officer_ts': 'Assigned Officer (Xitsonga)',
            'assigned_station': 'Assigned Station / Xitlhangi lexi nyikiweke',
        }


class OfficerNoteForm(forms.Form):
    """Form for officers to add notes"""
    officer_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Add investigation notes, updates, or actions taken...'}),
        required=False,
        label='Officer Notes / Nhlamuselo ya Ofisara'
    )
    officer_notes_ts = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Nhlamuselo ya Ofisara hi Xitsonga...'}),
        required=False,
        label='Officer Notes (Xitsonga) / Nhlamuselo ya Ofisara hi Xitsonga'
    )