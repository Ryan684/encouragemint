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
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from backend.src.views.garden_viewset import GardenViewSet
from backend.src.views.login_view import login
from backend.src.views.plant_detail_view import plant_detail
from backend.src.views.plant_viewset import PlantViewSet
from backend.src.views.user_viewset import UserViewSet

router = DefaultRouter()
router.register(r"user", UserViewSet)
router.register(r"garden", GardenViewSet)
router.register(r"plant", PlantViewSet)

urlpatterns = [
    url(r"^plant_detail/(?P<trefle_id>.+)/$", plant_detail),
    url(r"^login/$", login)
]

urlpatterns += router.urls
