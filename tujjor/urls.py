from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/',include('django.conf.urls.i18n')),
    path('ckeditor/',include('ckeditor_uploader.urls')),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
