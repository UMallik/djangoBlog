from django.urls import path
from .views import *

app_name='cadmin-api'
urlpatterns = [
    path('register/',UserCreateAPIView.as_view(), name='user-register'),
    path('login/',UserLoginAPIView.as_view(), name='user-login'),

    
    
]