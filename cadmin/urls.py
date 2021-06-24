from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'cadmin'

urlpatterns = [
    path('activate/account/', views.activate_account, name = 'activate'),
    path('register/', views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name = 'cadmin/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'cadmin/logout.html'), name = 'logout'),
    
    
    path('profile/',views.profile,name= 'profile'),
 



]