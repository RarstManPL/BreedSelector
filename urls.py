from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('prediction/', include('apps.prediction.urls')),
    path('api/', include('apps.api.urls')),

    path('admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),

    path('settings/', include('livesettings.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

