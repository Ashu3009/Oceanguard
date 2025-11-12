from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.base import ContentFile
from .models import BoatCapture
import datetime

@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        img_data = request.body
        
        # Create filename
        filename = f"capture_{int(datetime.datetime.now().timestamp())}.jpg"
        
        # Save to database using Django model
        boat_capture = BoatCapture()
        boat_capture.image.save(filename, ContentFile(img_data), save=True)
        
        print(f"✅ Image Saved to DB: {boat_capture.id} - {filename}")
        
        return JsonResponse({
            "status": "received",
            "id": boat_capture.id,
            "filename": filename
        })
    
    return JsonResponse({"error": "POST only"})


def gallery(request):
    # Get all boat captures from database
    captures = BoatCapture.objects.all()
    
    # Calculate stats
    total = captures.count()
    pending = captures.filter(status='pending').count()
    approved = captures.filter(status='approved').count()
    warnings = captures.filter(status='warning').count()
    
    return render(request, "gallery.html", {
        "captures": captures,
        "total": total,
        "pending": pending,
        "approved": approved,
        "warnings": warnings,
    })



@csrf_exempt
def update_status(request, capture_id):
    if request.method == "POST":
        try:
            import json
            from django.utils import timezone
            
            # Get the capture
            capture = BoatCapture.objects.get(id=capture_id)
            
            # Get data from request
            data = json.loads(request.body)
            new_status = data.get('status')
            reviewed_by = data.get('reviewed_by', 'Coast Guard')
            
            # Update status
            capture.status = new_status
            capture.reviewed_by = reviewed_by
            capture.reviewed_at = timezone.now()
            capture.save()
            
            print(f"✅ Status Updated: Capture #{capture_id} → {new_status}")
            
            return JsonResponse({
                "success": True,
                "message": f"Status updated to {new_status}"
            })
            
        except BoatCapture.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": "Capture not found"
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })
    
    return JsonResponse({"error": "POST only"})
