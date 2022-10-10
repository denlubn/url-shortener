from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from url_shortener.models import URL


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ["id", "original_link", "short_url", "num_visits"]
        read_only_fields = ["id", "short_url", "num_visits"]


class UrlListAdminSerializer(URLSerializer):
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field="email")

    class Meta(URLSerializer.Meta):
        fields = URLSerializer.Meta.fields + ["user"]


class URLDetailSerializer(URLSerializer):
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field="email")
    short_url = serializers.CharField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=URL.objects.all())
        ]
    )

    class Meta:
        model = URL
        fields = "__all__"
        read_only_fields = ["num_visits"]
