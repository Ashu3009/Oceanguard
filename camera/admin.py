from django.contrib import admin
from .models import BoatCapture

@admin.register(BoatCapture)
class BoatCaptureAdmin(admin.ModelAdmin):
    list_display = ['id', 'captured_at', 'qr_detected', 'qr_valid', 'status', 'reviewed_by']
    list_filter = ['status', 'qr_valid', 'qr_detected']
    search_fields = ['qr_data', 'notes']
    readonly_fields = ['captured_at', 'image']
    
    fieldsets = (
        ('Image Info', {
            'fields': ('image', 'captured_at')
        }),
        ('QR Code Details', {
            'fields': ('qr_detected', 'qr_data', 'qr_valid')
        }),
        ('Coast Guard Review', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'notes')
        }),
    )

from .models import RegisteredBoat, QRScanLog

@admin.register(RegisteredBoat)
class RegisteredBoatAdmin(admin.ModelAdmin):
    list_display = ['boat_id', 'boat_name', 'owner_name', 'total_entries', 'suspicious_activity_count', 'is_blacklisted']
    list_filter = ['is_blacklisted']
    search_fields = ['boat_id', 'boat_name', 'owner_name', 'qr_code']
    readonly_fields = ['total_entries', 'suspicious_activity_count', 'last_seen_at', 'qr_last_used']

@admin.register(QRScanLog)
class QRScanLogAdmin(admin.ModelAdmin):
    list_display = ['boat', 'scanned_at', 'calculated_speed', 'is_suspicious']
    list_filter = ['is_suspicious', 'scanned_at']
    search_fields = ['boat__boat_id', 'boat__boat_name']
    readonly_fields = ['scanned_at', 'distance_from_last_scan', 'time_since_last_scan', 'calculated_speed']
