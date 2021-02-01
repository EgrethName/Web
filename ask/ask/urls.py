"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, re_path

urlpatterns = [
    re_path('qa/', include('qa.urls')),
    re_path('admin/', admin.site.urls),
    re_path('', include('qa.urls')),
    re_path('login/', include('qa.urls')),
    re_path('signup/', include('qa.urls')),
    re_path('ask/', include('qa.urls')),
    re_path(r'question/\d+/', include('qa.urls')),
    re_path('popular/', include('qa.urls')),
    re_path('new/', include('qa.urls')),
]
