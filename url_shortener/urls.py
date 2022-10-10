from django.urls import path, include
from rest_framework import routers

from url_shortener.views import URLViewSet, RedirectView

router = routers.DefaultRouter()
router.register("urls", URLViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("<str:slug>/", RedirectView.as_view(), name="redirect"),
]

app_name = "url_shortener"
