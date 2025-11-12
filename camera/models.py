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