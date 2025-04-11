"""
URL configuration for c7_motors project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path , include
from c7_app import views as c7_motors_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView 
from c7_app.admin import custom_admin_site 

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', include('c7_app.urls')),
]


custom_admin_site.index_title = "C7 Motors"
custom_admin_site.site_header = "C7 Motors Administration"

urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
