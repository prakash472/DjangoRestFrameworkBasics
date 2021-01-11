from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import PostSerializer, CategoriesSerializer, PostCategorySerializer
from .models import DemoPost, Categories
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS
from rest_framework import generics, permissions


class CreatePostUserPermission(BasePermission):
    message = "Editing posts is restricted to the author of the post only."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class PostList(APIView):
    def get(self, request):
        posts = DemoPost.objects.all()
        serializer = PostCategorySerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostSearch(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = DemoPost.objects.all()
    serializer_class = PostCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^slug"]


class CreatePost(generics.CreateAPIView, CreatePostUserPermission):
    permission_classes = [
        permissions.IsAuthenticated, CreatePostUserPermission]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return DemoPost.objects.filter(author=user)


class UserPostDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostCategorySerializer
    queryset = DemoPost.objects.all()


class EditPost(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return DemoPost.objects.filter(author=user)


class DeletePost(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return DemoPost.objects.filter(author=user)
