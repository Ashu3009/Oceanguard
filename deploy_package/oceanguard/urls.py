"""
URL configuration for oceanguard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from camera.views import (
    upload_image,
    gallery,
    approved_gallery,
    warning_gallery,
    update_status,
    delete_capture
)
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/gallery/', permanent=False)),
    path('admin/', admin.site.urls),

    # Image Upload
    path('upload-image/', upload_image, name='upload_image'),

    # Gallery Pages
    path('gallery/', gallery, name='gallery'),
    path('approved/', approved_gallery, name='approved_gallery'),
    path('warnings/', warning_gallery, name='warning_gallery'),

    # Actions
    path('update-status/<int:capture_id>/', update_status, name='update_status'),
    path('delete-capture/<int:capture_id>/', delete_capture, name='delete_capture'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)