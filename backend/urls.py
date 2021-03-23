from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from backend.views import RecommendView

router = DefaultRouter()

urlpatterns = [
    url(r"^recommend/$", RecommendView.as_view())
]

urlpatterns += router.urls
