from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """Custom user model for MySAPS Tzaneen Connect"""
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ts', 'Xitsonga'),
        ('nso', 'Sepedi'),
        ('ve', 'TshiVenda'),
    ]
    
    # Contact information
    phone_number = models.CharField(max_length=15, unique=True, help_text=_('Cellphone number for notifications'))
    id_number = models.CharField(max_length=13, blank=True, null=True)
    
    # Address information
    street_address = models.TextField(blank=True, null=True)
    suburb = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, default='Tzaneen')
    province = models.CharField(max_length=50, default='Limpopo')
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    
    # Preferences
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    notification_method = models.CharField(max_length=20, choices=[
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('both', 'Both')
    ], default='whatsapp')
    
    # Accessibility
    large_font = models.BooleanField(default=False)
    voice_input = models.BooleanField(default=False)
    
    # Location
    default_location_lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    default_location_lng = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    
    # Business details
    is_business_owner = models.BooleanField(default=False)
    business_name = models.CharField(max_length=200, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.phone_number})"
    
    def get_notification_methods(self):
        """Return list of notification methods"""
        if self.notification_method == 'both':
            return ['sms', 'whatsapp']
        return [self.notification_method]