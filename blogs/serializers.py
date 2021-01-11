from rest_framework import serializers
from .models import DemoPost, Categories
from rest_framework.serializers import PrimaryKeyRelatedField


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoPost
        fields = ["id", "title", "content", "date_posted", "excerpt", "slug",
                  "review_positive", "image", "author", "categories"]


class PostCategorySerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(many=True)

    class Meta:
        model = DemoPost
        fields = ["id", "title", "content", "date_posted", "excerpt", "slug",
                  "review_positive", "image", "author", "categories"]
