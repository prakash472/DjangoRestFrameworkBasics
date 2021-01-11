from django.urls import path,include
from . import views
#from .views import PostList,PostDetail
from .views import PostViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('post',PostViewSet, basename="post")

urlpatterns = [
    path('viewset/',include(router.urls)),
    path('viewset/<int:pk>/',include(router.urls)),
    #path('', views.),
    #path('post_details/<int:pk>/',views.post_details),
    #path('',PostList.as_view()),
    #path('post_details/<int:pk>/',PostDetail.as_view()),
]
