"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from administration.views import intranet
from administration.views import forgot_password,Logout,unauthorized

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public.urls')),
    path('administration/', include('administration.urls')),
    path('patient/', include('patient.urls')),
    path('doctor/', include('doctor.urls')),
    path('staff/', include('staff.urls')),
    path('intranet', intranet, name ='intranet'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('logout', Logout, name='logout'),
    path('unauthorized', unauthorized, name='unauthorized'),
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
