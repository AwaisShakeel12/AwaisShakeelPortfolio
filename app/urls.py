from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('project', views.project, name='project'),
    path('likeproject', views.likeproject, name='likeproject'),
    path('community', views.community, name='community'),
    path('communitypostdetail/<str:pk>/', views.community_post_detail, name='community_post_detail'),
    path('deletecommunity/<str:pk>/', views.deletecommunity, name='deletecommunity'),
    path('deletefeedback/<str:pk>/', views.deletefeedback, name='deletefeedback'),


]