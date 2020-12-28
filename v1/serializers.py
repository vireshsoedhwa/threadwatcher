from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import URLValidator

from .models import Thread

# def validate_url(self, value):
#     if 'django' not in value.lower():
#         raise serializers.ValidationError("Blog post is not about Django")
#     return value

class ThreadSerializer(serializers.Serializer):

    threadid = serializers.DecimalField(validators=[UniqueValidator], max_digits=12, decimal_places=0)
    summary = serializers.CharField(max_length=1000, min_length=None, allow_blank=True, allow_null=True, required=False)

    def create(self, validated_data):
        thread = Thread.objects.create(**validated_data)
        thread.create_urlid()
        return thread

    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance
    