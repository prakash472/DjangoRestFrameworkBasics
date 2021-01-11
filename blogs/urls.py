from django.urls import path
from .views import PostList, PostSearch, CreatePost, EditPost, UserPostDetail, DeletePost
urlpatterns = [
    path('posts/', PostList.as_view()),
    path('search/', PostSearch.as_view()),
    path('user/create/', CreatePost.as_view(), name="create_post"),
    path('user/edit/posts/<int:pk>',
         UserPostDetail.as_view(), name="user_post_detail"),
    path('user/delete/posts/<int:pk>', DeletePost.as_view(), name="delete_post")

]
