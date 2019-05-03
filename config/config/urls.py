from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('apps.user.urls', namespace='user')),
    path('', include('apps.core.urls', namespace='core')),
]
