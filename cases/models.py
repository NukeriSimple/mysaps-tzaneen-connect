from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from accounts.models import CustomUser
import uuid

class IncidentCategory(models.Model):
    """Incident categories"""
    
    CATEGORY_TYPES = [
        ('theft', 'Theft / Vutsotsi'),
        ('burglary', 'Burglary / Ku ngheneriwa endlwini'),
        ('assault', 'Assault / Ku vuriwa'),
        ('robbery', 'Robbery / Ku khomeriwa'),
        ('property_damage', 'Property Damage / Ku onhakala ka xifaniso'),
        ('domestic_violence', 'Domestic Violence / Nghungu ya le kaya'),
        ('service_delivery', 'Service Delivery / Vukorhokeri'),
        ('other', 'Other / Swin\'wana'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_TYPES, unique=True)
    icon = models.CharField(max_length=50, default='fas fa-exclamation-triangle')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Incident Category')
        verbose_name_plural = _('Incident Categories')
    
    def __str__(self):
        return self.get_name_display()


class Case(models.Model):
    """Case model for tracking incidents"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending / Ku lindzela'),
        ('assigned', 'Assigned / Ku nyikiwile'),
        ('in_progress', 'In Progress / Ku endliwa'),
        ('resolved', 'Resolved / Ku lulamisiwile'),
        ('closed', 'Closed / Ku pfariwile'),
    ]
    
    # Case identification
    case_number = models.CharField(max_length=20, unique=True, editable=False)
    reference_number = models.CharField(max_length=20, blank=True, null=True, help_text=_('SAPS case reference number'))
    
    # Relationships
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cases')
    category = models.ForeignKey(IncidentCategory, on_delete=models.SET_NULL, null=True, related_name='cases')
    
    # Incident details
    title = models.CharField(max_length=200)
    description = models.TextField(validators=[MinLengthValidator(10)])
    description_xitsonga = models.TextField(blank=True, null=True)
    
    # Location
    location_lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    location_lng = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    location_description = models.TextField(help_text=_('Describe location using landmarks if GPS not available'))
    
    # Contact details
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(blank=True, null=True)
    
    # Evidence
    has_photo_evidence = models.BooleanField(default=False)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_officer = models.CharField(max_length=100, blank=True, null=True)
    assigned_station = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('Case')
        verbose_name_plural = _('Cases')
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.case_number:
            import datetime
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            random_part = str(uuid.uuid4().hex[:4].upper())
            self.case_number = f"TZN-CAS-{date_str}-{random_part}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.case_number} - {self.title}"
    
    def get_status_color(self):
        """Return CSS class for status indicator"""
        colors = {
            'pending': 'warning',
            'assigned': 'info',
            'in_progress': 'primary',
            'resolved': 'success',
            'closed': 'secondary',
        }
        return colors.get(self.status, 'secondary')
    
    def get_status_display_bilingual(self):
        """Return bilingual status display"""
        status_map = {
            'pending': 'Pending / Ku lindzela',
            'assigned': 'Assigned / Ku nyikiwile',
            'in_progress': 'In Progress / Ku endliwa',
            'resolved': 'Resolved / Ku lulamisiwile',
            'closed': 'Closed / Ku pfariwile',
        }
        return status_map.get(self.status, self.status)


class CaseUpdate(models.Model):
    """Track case updates and timeline"""
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='updates')
    update_text = models.TextField()
    update_text_xitsonga = models.TextField(blank=True, null=True)
    update_type = models.CharField(max_length=20, choices=[
        ('status_change', 'Status Change'),
        ('officer_note', 'Officer Note'),
        ('user_followup', 'User Follow-up'),
        ('evidence_added', 'Evidence Added'),
        ('resolution', 'Resolution'),
    ])
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='case_updates')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Case Update')
        verbose_name_plural = _('Case Updates')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.case.case_number} - {self.update_type} - {self.created_at}"


class Evidence(models.Model):
    """Evidence attached to cases"""
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='evidence')
    image = models.ImageField(upload_to='evidence/%Y/%m/%d/')
    caption = models.CharField(max_length=500, blank=True)
    caption_xitsonga = models.CharField(max_length=500, blank=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Evidence')
        verbose_name_plural = _('Evidence')
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Evidence for {self.case.case_number}"


class PoliceStation(models.Model):
    """Police station information"""
    
    name = models.CharField(max_length=200)
    name_xitsonga = models.CharField(max_length=200, blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    emergency_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    location_lat = models.DecimalField(max_digits=10, decimal_places=7)
    location_lng = models.DecimalField(max_digits=10, decimal_places=7)
    operating_hours = models.TextField()
    is_satellite = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Police Station')
        verbose_name_plural = _('Police Stations')
    
    def __str__(self):
        return self.name


class Notification(models.Model):
    """Notifications for users"""
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    message_xitsonga = models.TextField(blank=True)
    notification_type = models.CharField(max_length=20, choices=[
        ('status_update', 'Status Update'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
        ('info', 'Information'),
    ])
    is_read = models.BooleanField(default=False)
    sent_via_sms = models.BooleanField(default=False)
    sent_via_whatsapp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} - {self.title}"