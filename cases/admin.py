from django.contrib import admin
from .models import IncidentCategory, Case, CaseUpdate, Evidence, PoliceStation, Notification

@admin.register(IncidentCategory)
class IncidentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ts', 'is_active')
    list_filter = ('is_active',)
    fieldsets = (
        ('English', {'fields': ('name',)}),
        ('Xitsonga', {'fields': ('name_ts',)}),
        ('Other', {'fields': ('icon', 'is_active')}),
    )

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'user', 'title', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('case_number', 'title', 'title_ts', 'user__username')
    readonly_fields = ('case_number',)
    fieldsets = (
        ('Case Information', {'fields': ('case_number', 'user', 'category')}),
        ('English', {'fields': ('title', 'description', 'location_description')}),
        ('Xitsonga', {'fields': ('title_ts', 'description_ts', 'location_description_ts')}),
        ('Contact', {'fields': ('contact_name', 'contact_phone', 'contact_email')}),
        ('Status', {'fields': ('status', 'assigned_officer', 'assigned_station')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'resolved_at')}),
    )

@admin.register(CaseUpdate)
class CaseUpdateAdmin(admin.ModelAdmin):
    list_display = ('case', 'update_type', 'created_by', 'created_at')
    list_filter = ('update_type', 'created_at')
    fieldsets = (
        ('English', {'fields': ('update_text',)}),
        ('Xitsonga', {'fields': ('update_text_ts',)}),
    )

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('case', 'uploaded_by', 'uploaded_at')
    fieldsets = (
        ('English', {'fields': ('caption',)}),
        ('Xitsonga', {'fields': ('caption_ts',)}),
    )

@admin.register(PoliceStation)
class PoliceStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'name_ts')
    fieldsets = (
        ('English', {'fields': ('name', 'address', 'operating_hours')}),
        ('Xitsonga', {'fields': ('name_ts', 'address_ts', 'operating_hours_ts')}),
        ('Contact', {'fields': ('phone', 'emergency_phone', 'email')}),
        ('Location', {'fields': ('location_lat', 'location_lng')}),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    fieldsets = (
        ('English', {'fields': ('title', 'message')}),
        ('Xitsonga', {'fields': ('title_ts', 'message_ts')}),
    )