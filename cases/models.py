from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from accounts.models import CustomUser
import uuid

class IncidentCategory(models.Model):
    """Incident categories with bilingual support"""
    
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
    name_ts = models.CharField(max_length=100, blank=True, verbose_name="Name in Xitsonga")
    icon = models.CharField(max_length=50, default='fas fa-exclamation-triangle')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Incident Category')
        verbose_name_plural = _('Incident Categories')
    
    def __str__(self):
        return self.get_name_display()
    
    def get_name_in_language(self, language='en'):
        """Get category name in specified language"""
        if language == 'ts' and self.name_ts:
            return self.name_ts
        return self.get_name_display()


class Case(models.Model):
    """Case model with bilingual support"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending / Ku lindzela'),
        ('assigned', 'Assigned / Ku nyikiwile'),
        ('in_progress', 'In Progress / Ku endliwa'),
        ('resolved', 'Resolved / Ku lulamisiwile'),
        ('closed', 'Closed / Ku pfariwile'),
    ]
    
    # Case identification
    case_number = models.CharField(max_length=20, unique=True, editable=False)
    reference_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Relationships
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cases')
    category = models.ForeignKey(IncidentCategory, on_delete=models.SET_NULL, null=True, related_name='cases')
    
    # Incident details - English
    title = models.CharField(max_length=200)
    description = models.TextField(validators=[MinLengthValidator(10)])
    
    # Incident details - Xitsonga
    title_ts = models.CharField(max_length=200, blank=True, null=True, verbose_name="Title in Xitsonga")
    description_ts = models.TextField(blank=True, null=True, verbose_name="Description in Xitsonga")
    
    # Location
    location_lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    location_lng = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    location_description = models.TextField()
    location_description_ts = models.TextField(blank=True, null=True, verbose_name="Location in Xitsonga")
    
    # Contact details
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_officer = models.CharField(max_length=100, blank=True, null=True)
    assigned_station = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
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
        colors = {
            'pending': 'warning',
            'assigned': 'info',
            'in_progress': 'primary',
            'resolved': 'success',
            'closed': 'secondary',
        }
        return colors.get(self.status, 'secondary')
    
    def get_status_display_bilingual(self, language='en'):
        """Get bilingual status display"""
        status_map = {
            'pending': {'en': 'Pending', 'ts': 'Ku lindzela'},
            'assigned': {'en': 'Assigned', 'ts': 'Ku nyikiwile'},
            'in_progress': {'en': 'In Progress', 'ts': 'Ku endliwa'},
            'resolved': {'en': 'Resolved', 'ts': 'Ku lulamisiwile'},
            'closed': {'en': 'Closed', 'ts': 'Ku pfariwile'},
        }
        return status_map.get(self.status, {}).get(language, self.status)
    
    def get_title(self, language='en'):
        """Get title in specified language"""
        if language == 'ts' and self.title_ts:
            return self.title_ts
        return self.title
    
    def get_description(self, language='en'):
        """Get description in specified language"""
        if language == 'ts' and self.description_ts:
            return self.description_ts
        return self.description
    
    def get_location(self, language='en'):
        """Get location in specified language"""
        if language == 'ts' and self.location_description_ts:
            return self.location_description_ts
        return self.location_description


class CaseUpdate(models.Model):
    """Case updates with bilingual support"""
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='updates')
    update_text = models.TextField(verbose_name="Update in English")
    update_text_ts = models.TextField(blank=True, null=True, verbose_name="Update in Xitsonga")
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
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.case.case_number} - {self.update_type} - {self.created_at}"
    
    def get_update_text(self, language='en'):
        """Get update text in specified language"""
        if language == 'ts' and self.update_text_ts:
            return self.update_text_ts
        return self.update_text


class Evidence(models.Model):
    """Evidence attached to cases"""
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='evidence')
    image = models.ImageField(upload_to='evidence/%Y/%m/%d/')
    caption = models.CharField(max_length=500, blank=True)
    caption_ts = models.CharField(max_length=500, blank=True, verbose_name="Caption in Xitsonga")
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Evidence for {self.case.case_number}"


class PoliceStation(models.Model):
    """Police station with bilingual support"""
    
    name = models.CharField(max_length=200, verbose_name="Name in English")
    name_ts = models.CharField(max_length=200, blank=True, verbose_name="Name in Xitsonga")
    address = models.TextField(verbose_name="Address in English")
    address_ts = models.TextField(blank=True, verbose_name="Address in Xitsonga")
    phone = models.CharField(max_length=20)
    emergency_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    location_lat = models.DecimalField(max_digits=10, decimal_places=7)
    location_lng = models.DecimalField(max_digits=10, decimal_places=7)
    operating_hours = models.TextField(verbose_name="Hours in English")
    operating_hours_ts = models.TextField(blank=True, verbose_name="Hours in Xitsonga")
    is_satellite = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Police Station'
        verbose_name_plural = 'Police Stations'
    
    def __str__(self):
        return self.name
    
    def get_name(self, language='en'):
        """Get name in specified language"""
        if language == 'ts' and self.name_ts:
            return self.name_ts
        return self.name
    
    def get_address(self, language='en'):
        """Get address in specified language"""
        if language == 'ts' and self.address_ts:
            return self.address_ts
        return self.address
    
    def get_hours(self, language='en'):
        """Get hours in specified language"""
        if language == 'ts' and self.operating_hours_ts:
            return self.operating_hours_ts
        return self.operating_hours


class Notification(models.Model):
    """Notifications with bilingual support"""
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=200, verbose_name="Title in English")
    title_ts = models.CharField(max_length=200, blank=True, verbose_name="Title in Xitsonga")
    message = models.TextField(verbose_name="Message in English")
    message_ts = models.TextField(blank=True, verbose_name="Message in Xitsonga")
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
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} - {self.title}"
    
    def get_title(self, language='en'):
        """Get title in specified language"""
        if language == 'ts' and self.title_ts:
            return self.title_ts
        return self.title
    
    def get_message(self, language='en'):
        """Get message in specified language"""
        if language == 'ts' and self.message_ts:
            return self.message_ts
        return self.message