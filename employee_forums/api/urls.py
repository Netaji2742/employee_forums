from django.urls import path
from .views import *
from knox import views as knox_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    #path('login/', csrf_exempt(knox_views.LoginView.as_view()), name='knox_login'),
    path('login/', LoginAPI.as_view(), name='knox_login'),

    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    
    path('profile/', ProfileUpdateAPI.as_view()),
    path('posts/', PostListAPI.as_view()),
    path('posts/create/', PostCreateAPI.as_view()),
    path('posts/<int:post_id>/like/', LikePostAPI.as_view()),
    path('posts/<int:post_id>/unlike/', UnlikePostAPI.as_view()),
    path('connections/send/<int:to_user_id>/', SendConnectionRequestAPI.as_view()),
    path('connections/requests/', ConnectionRequestsAPI.as_view()),
    path('connections/accept/<int:conn_id>/', AcceptConnectionAPI.as_view()),
    path('recommendations/', RecommendUsersAPI.as_view()),
]
