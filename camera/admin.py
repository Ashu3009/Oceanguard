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