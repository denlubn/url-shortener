import uuid

from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from url_shortener.models import URL
from url_shortener.serializers import URLSerializer, URLDetailSerializer, UrlListAdminSerializer


class URLPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 100


class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all().select_related("user")
    serializer_class = URLSerializer
    pagination_class = URLPagination
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["retrieve", "update", "partial_update"]:
            return URLDetailSerializer
        if self.action == "list" and self.request.user.is_superuser:
            return UrlListAdminSerializer

        return URLSerializer

    def perform_create(self, serializer):
        short_url = "localhost:8000/" + str(uuid.uuid4())[:5]
        serializer.save(short_url=short_url, user=self.request.user)


class RedirectView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def redirect(request, slug):
        url = URL.objects.get(short_url=f"localhost:8000/{slug}")
        url.num_visits += 1
        url.save()
        return HttpResponseRedirect(redirect_to=url.original_link)

    def get(self, request, slug):
        return self.redirect(request, slug)
