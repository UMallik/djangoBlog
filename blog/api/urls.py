from django.urls import path
from .views import *

app_name='blog-api'
urlpatterns = [
    path('',PostListAPIView.as_view(), name='post-list'),
    path('create/', PostCreateAPIView.as_view(), name = 'post-create'),
    path('<slug:slug>/',PostDetailAPIView.as_view(),name='post-detail'),
    path('update/<slug:slug>/',PostUpdateAPIView.as_view(),name='post-update'),
    path('delete/<slug:slug>/',PostDeleteAPIView.as_view(),name='post-delete'),
    
]