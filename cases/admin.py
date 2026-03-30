from django.contrib import admin
from .models import IncidentCategory, Case, CaseUpdate, Evidence, PoliceStation, Notification

@admin.register(IncidentCategory)
class IncidentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'user', 'title', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('case_number', 'title', 'user__username')
    readonly_fields = ('case_number',)

@admin.register(CaseUpdate)
class CaseUpdateAdmin(admin.ModelAdmin):
    list_display = ('case', 'update_type', 'created_by', 'created_at')
    list_filter = ('update_type', 'created_at')

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('case', 'uploaded_by', 'uploaded_at')

@admin.register(PoliceStation)
class PoliceStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'location_lat', 'location_lng')
    search_fields = ('name',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')