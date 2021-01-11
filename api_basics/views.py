from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,Http404
from rest_framework.parsers import JSONParser
from api_basics.serializers import PostSerializer
from api_basics.models import Post
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

"""
#Tutorial-1:Serialization
# It is the function based view. However, there are different approaches to it also
@csrf_exempt
def post_list(request):
    if request.method == "GET":
        posts=Post.objects.all()
        serializer=PostSerializer(posts,many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method=="POST":
        data=JSONParser().parse(request)
        serializer=PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        else:
            return JsonResponse(serializer.errors,status=400)

@csrf_exempt
def post_details(request,pk):
    try:
        post=Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse(status=404)

    if request.method=="GET":
        serializer=PostSerializer(post)
        return JsonResponse(serializer.data,status=201)
    elif request.method=="PUT":
        data=JSONParser().parse(request)
        serializer=PostSerializer(post,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors,status=400)
    elif request.method=="DELETE":
        post.delete()
        return HttpResponse(status=204)

"""

"""
# Instead of Function based view we can use the @api_view decorator which has many benifits. It returns Response 
# instead of Django Response and we can also access Browsable APIs Lateron.


# Tutorial-2: Request and responses
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET','POST'])
def post_list(request):
    if request.method=="GET":
        post=Post.objects.all()
        serializer=PostSerializer(post,many=True)
        return Response(serializer.data)
    elif request.method=="POST":
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK )
        return Response(serializer.errors,status=status.HTTP_400_ERROR)

@api_view(["GET","DELETE","PUT"])
def post_details(request,pk):
    try:
        post=Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=="GET":
        serializer=PostSerializer(post)
        return Response(serializer.data)
    elif request.method=="PUT":
        serializer=PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.ERROR)
    elif request.method=="DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
"""

"""
Tutorial-3
# We can use class based View to keep our code organized. It is present inside the views of django_restframework. 
# Previously in function based we have used decorators api_view now we are using View APIView.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PostList(APIView):
    def get(self,request):
        posts=Post.objects.all()
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=PostSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_ERROR)

class PostDetail(APIView):
    def get_object(self,pk):
        try:
            post=Post.objects.get(pk=pk)
            return post
        except Post.DoesNotExist:
            raise Http404
    
    def get(self,request,pk):
        post=self.get_object(pk)
        serializer=PostSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        post=self.get_object(pk)
        serializer=PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_ERROR)
    
    def delete(self,request,pk):
        post=self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

"""
Tutorial-4
# In order to simply our tasks we can also use generics views and mixins provided by the django_rest_framewoek

from rest_framework import generics
from rest_framework import mixins
class PostList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class PostDetail(generics.GenericAPIView,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin):
    queryset=Post.objects.all()
    serializer_class=PostSerializer


    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
"""

"""
# Tutorial-4 (Authentication and Permissions)
# Basic Authentication: Uses Http Basic Authentication. Used for username and Password login. Advised for Basic Authentication
# Token Authentication: When we want to access API through mobile apps like android or ios Apps or desktop native application
# Session Authentication: Uses Django's default session background. It is appropriate for AJAX clients that are running in the same session.
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import mixins

class PostList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    #authentication_classes=[SessionAuthentication,BasicAuthentication]
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class PostDetail(generics.GenericAPIView,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin):
    queryset=Post.objects.all()
    serializer_class=PostSerializer


    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

"""
# ----------------------------------------------------------------
"""
There are generally two helper classes that django rest framework provides to create our API end-points.
They are APIView and Viewset.
-------------------------------------
APIView- It helps us to create the API endpoints using the standard Methods for functions.
E.g. Uses method GET=To get item, POST=To create a item, PUT= To update an item, PATCH= To partially update an item, Destroy=
- Gives most control over the logic and perfect for implementing complex logic, calling other APIs and other complex tasks
- Used for complex tasks described above.
------------------------------------------------
Viewsets- It helps us to write logic of our APIs endpoinds. It does not uses the standard HTTP methods but rather uses the methods that maps to the common API object actions like:
            List- Getting list of objects
            Create- Creating a object
            Retrieve- Getting a specific object
            Update- Update a specific object
            Partial Update- Partially update a specific object
            Destroy- To delete a object

- Used==> - Need to perform simple CRUD interface
          - Build quick and simple API
          - Less computational Logic.
------------------------------------------------------------
Let's work with routers and viewsets
"""
"""
# Using viewsets.Viewset
# if we are using viewsets.ViewSet, we need add all the functionalities, just like we did in our serializers class when we used serializers.Serializer instead of serializers.ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
class PostViewSet(viewsets.ViewSet):
    def list(self,request):
        posts=Post.objects.all()
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_ERROR)

    def retrieve(self,request,pk):
        all_posts=Post.objects.all()
        post=get_object_or_404(all_posts,pk=pk)
        serializer=PostSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def update(self,request,pk):
        post=Post.objects.get(pk=pk)
        serializer=PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_ERROR)

    def destroy(self,request,pk):
        try:
            post=Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

"""
# Using Generic Viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins

class PostViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,
                   mixins.CreateModelMixin, mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=PostSerializer
    queryset=Post.objects.all()
     
"""
#Using Model Viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins

class PostViewSet(viewsets.ModelViewSet):
    serializer_class=PostSerializer
    queryset=Post.objects.all()