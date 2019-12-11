"""encouragemint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from rest_framework.routers import DefaultRouter

from encouragemint.encouragemint.views import ProfileViewSet, PlantViewSet, GardenViewSet, add_plant

router = DefaultRouter()
router.register(r"profile", ProfileViewSet)
router.register(r"garden", GardenViewSet)
router.register(r"plant", PlantViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('add_plant/', add_plant),
]
