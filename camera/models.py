from django.db import models

# BoatCapture Model - Har boat ki photo aur uska status
class BoatCapture(models.Model):
    # Status choices for Coast Guard action
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),      # Abhi review nahi hua
        ('approved', 'OK - No Threat'),     # Coast Guard ne OK mark kiya
        ('warning', 'WARNING - Alert'),     # Coast Guard ne warning diya
    ]

    # Image and capture info
    image = models.ImageField(upload_to='captures/')
    captured_at = models.DateTimeField(auto_now_add=True)

    # QR Code validation
    qr_detected = models.BooleanField(default=False)  # QR mila ya nahi
    qr_data = models.TextField(blank=True, null=True)  # QR mein kya likha hai
    qr_valid = models.BooleanField(default=False)     # QR valid hai ya nahi

    # Coast Guard Review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.CharField(max_length=100, blank=True, null=True)  # Kaun ne review kiya
    notes = models.TextField(blank=True, null=True)  # Additional notes

    class Meta:
        ordering = ['-captured_at']  # Latest first
        verbose_name = 'Boat Capture'
        verbose_name_plural = 'Boat Captures'

    def __str__(self):
        return f"Capture {self.id} - {self.status} at {self.captured_at.strftime('%Y-%m-%d %H:%M:%S')}"
    

# Registered Boats Database
class RegisteredBoat(models.Model):
    boat_id = models.CharField(max_length=50, unique=True)  # e.g., "BOAT-12345"
    boat_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    
    # QR Code Info
    qr_code = models.CharField(max_length=200, unique=True)
    qr_last_used = models.DateTimeField(null=True, blank=True)
    
    # GPS Tracking
    last_latitude = models.FloatField(null=True, blank=True)
    last_longitude = models.FloatField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    
    # Security Stats
    total_entries = models.IntegerField(default=0)
    suspicious_activity_count = models.IntegerField(default=0)
    is_blacklisted = models.BooleanField(default=False)
    
    # Boat Image for verification
    boat_image = models.ImageField(upload_to='boats/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Registered Boat'
        verbose_name_plural = 'Registered Boats'
    
    def __str__(self):
        return f"{self.boat_id} - {self.boat_name}"


# QR Scan History - Tracking har scan
class QRScanLog(models.Model):
    boat = models.ForeignKey(RegisteredBoat, on_delete=models.CASCADE, related_name='scan_logs')
    capture = models.ForeignKey(BoatCapture, on_delete=models.CASCADE, null=True, blank=True)
    
    scanned_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Calculated metrics
    distance_from_last_scan = models.FloatField(null=True, blank=True)  # in km
    time_since_last_scan = models.FloatField(null=True, blank=True)     # in minutes
    calculated_speed = models.FloatField(null=True, blank=True)         # in km/h
    
    is_suspicious = models.BooleanField(default=False)
    suspicion_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-scanned_at']
    
    def __str__(self):
        return f"{self.boat.boat_id} - {self.scanned_at}"
