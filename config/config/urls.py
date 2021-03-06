from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

MEDIA_FILE_PATHS = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('apps.user.urls', namespace='user')),
    path('', include('apps.core.urls', namespace='core')),
] + MEDIA_FILE_PATHS
