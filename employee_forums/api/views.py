from django.shortcuts import render

# Create your views here.

from rest_framework.authentication import TokenAuthentication
from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from rest_framework.permissions import IsAuthenticated


from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics



from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .models import UserProfile, Post, Like, Connection
from .serializers import *

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })

class ProfileUpdateAPI(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)



#Post APIs
class PostCreateAPI(generics.CreateAPIView):
    serializer_class = PostSerializer
    #permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostListAPI(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    #permission_classes = [permissions.IsAuthenticated]

    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = [IsAuthenticated]


#Like/Unlike API

from rest_framework.views import APIView

class LikePostAPI(APIView):
    
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = [IsAuthenticated]

    #permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({"message": "Post liked"})
        else:
            return Response({"message": "Already liked"}, status=400)

class UnlikePostAPI(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            like = Like.objects.get(user=request.user, post_id=post_id)
            like.delete()
            return Response({"message": "Post unliked"})
        except Like.DoesNotExist:
            return Response({"message": "Like not found"}, status=404)


#Connection API
class SendConnectionRequestAPI(APIView):
    
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    #permission_classes = [permissions.IsAuthenticated]

    def post(self, request, to_user_id):
        to_user = User.objects.get(id=to_user_id)
        if Connection.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({"message": "Request already sent"}, status=400)
        Connection.objects.create(from_user=request.user, to_user=to_user)
        return Response({"message": "Connection request sent"})

class ConnectionRequestsAPI(generics.ListAPIView):
    serializer_class = ConnectionSerializer
    
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = [IsAuthenticated]

    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Connection.objects.filter(to_user=self.request.user, is_accepted=False)

class AcceptConnectionAPI(APIView):
    
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    #permission_classes = [permissions.IsAuthenticated]

    def post(self, request, conn_id):
        conn = Connection.objects.get(id=conn_id, to_user=request.user)
        conn.is_accepted = True
        conn.save()
        return Response({"message": "Connection accepted"})


#User Recommendation API
class RecommendUsersAPI(APIView):
    
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        my_connections = Connection.objects.filter(
            from_user=request.user, is_accepted=True
        ).values_list('to_user', flat=True)

        # Users connected to my connections
        suggested_users = Connection.objects.filter(
            from_user__in=my_connections, is_accepted=True
        ).exclude(to_user=request.user).values_list('to_user', flat=True).distinct()

        users = User.objects.filter(id__in=suggested_users).exclude(id=request.user.id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

'''''
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to the Social Media API!"})

'''

#adding custom login api




class LoginAPI(generics.GenericAPIView):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        from knox.models import AuthToken
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })


class ProfileUpdateAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

