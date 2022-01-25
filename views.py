from django.shortcuts import render
from ly3000projApp.models import Projects,Issue,User,Comment,Sprint
from ly3000projApp.serializers import ProjectsSerializer,IssueSerializer,UserSerializer,CommentSerializer,SprintSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, filters
from django.contrib.auth.models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
from ly3000projApp.serializers import UserSerializer, RegisterSerializer
from rest_framework import generics, permissions
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login,logout
from rest_framework.views import APIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework import status
from ly3000projApp.permissions import UserDesignationPermission,IssuePermission,SprintPermission
#from rest_framework import permissions





# Create your views here.

@api_view(['POST'])
def find_title(request):
        title = Projects.objects.filter(projectTitle=request.data['projectTitle'])
        serializer = ProjectsSerializer(title,many=True)
        return Response(serializer.data)

@api_view(['GET'])
def find_proj_list(request):
        proj_list = Projects.objects.all()
        serializer = ProjectsSerializer(proj_list,many=True)
        return Response(serializer.data)

@api_view(['GET'])
def find_issue_list(request):
        issue_list = Issue.objects.all()
        serializer = ProjectsSerializer(issue_list,many=True)
        return Response(serializer.data)

@api_view(['GET','POST','DELETE'])
def find_comment_list(request):
        comment_list = Comment.objects.all()
        serializer = CommentSerializer(comment_list,many=True)
        return Response(serializer.data)

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
class LoginAPI(APIView):
    #ermission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        logged_user = JSONWebTokenSerializer(data=request.data)
        if logged_user.is_valid():
            response_data = [{"JWT_Token":logged_user.validated_data.get('token')}]
            user = logged_user.validated_data['user']
            login(request, user)
            return Response({"msg":"Logged in Sucessfully","details":response_data},status=status.HTTP_200_OK)

        return Response(logged_user.errors,status=status.HTTP_400_BAD_REQUEST)

class LogoutAPI(APIView):
    #permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, format=None):
        logout(request)
        return Response({"msg":"Logged out Sucessfully"},status=status.HTTP_200_OK)

class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IssuePermission]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated,DjangoModelPermissions]
    #permission_classes = [UserDesignationPermission]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [SprintPermission,permissions.IsAuthenticated]
