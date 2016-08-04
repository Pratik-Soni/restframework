from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, renderers
from user_api.serializers import UserSerializer, GroupSerializer, UserDetailSerializer, UsersSerializer
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from user_api.models import UserDetails
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from user_api.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import detail_route


"""
class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
"""    
    
class GroupViewSet(viewsets.ModelViewSet):
    
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class JSONResponse(HttpResponse):
    #Render its content into JSON
    
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
    
        
@csrf_exempt
def user_list_old(request):
    
    if request.method == 'GET':
        users = UserDetails.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return JSONResponse(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
    
    
@csrf_exempt
def user_detail_old(request, pk):
    # Retrieve update delete user
    try:
        user = UserDetails.objects.get(pk=pk)
        
    except UserDetails.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return JSONResponse(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser.parse(request)
        serializer = UserDetailSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)
      
      

@api_view(['GET', 'POST'])
def users_list(request):
    if request.method == 'GET':
        users = UserDetails.objects.all()
        seriallizer = UserDetailSerializer(users, many=True)
        return Response(seriallizer.data)
    
    elif request.method == 'POST':
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    #Retrieve update Delete
    try:
        user = UserDetails.objects.get(pk=pk)
    except UserDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserDetailSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif  request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
       
       
class UsersList(APIView):
    
    def get(self, request, format=None):
        users = UserDetails.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserDetail(APIView):
    
    def get_object(self,pk):
        try:
            return UserDetails.objects.get(pk=pk)
        except UserDetails.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class NewUsersList(generics.ListAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class NewUserDetails(generics.RetrieveAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    
  
class UserListO(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    
class UserDetailO(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    
            
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    

class UserDetailViewSet(viewsets.ModelViewSet):
    
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    
    
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user.highlighted)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    