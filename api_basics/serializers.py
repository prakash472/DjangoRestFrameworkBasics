from rest_framework import serializers
from django.utils import timezone
from .models import Post

"""
# Using the serializers.Serializer
class PostSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=100)
    date_posted=serializers.DateTimeField(default=timezone.now)
    email=serializers.EmailField(max_length=100)
    content=serializers.CharField()

    def create(self, validated_data):
        return Post.objects.create(validated_data)
    
    def update(self,instance,validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.date_posted=validated_data.get('date_posted',instance.date_posted)
        instance.content=validated_data.get('content',instance.content)
        instance.email=validated_data.get('email',instance.email)
        instance.save()
        return instance
""" 
# We can user serializers.ModelSerializer like ModalForm
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=["id","title","email","content","date_posted"]