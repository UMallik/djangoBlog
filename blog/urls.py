from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, CategoryCreateView, UserCategoryView, TagCreateView, UserTagView
from . import views
from .sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'posts':PostSitemap
}

app_name = 'blog'

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name='sitemap'),
    path('save-session-data/', views.save_session_data, name='save_session_data'),
    path('access-session-data/', views.access_session_data, name='access_session_data'),
    path('delete-session-data/', views.delete_session_data, name='delete_session_data'),
    path('test-session/',views.test_session, name = 'test-session'),
    path('test-delete/',views.test_delete, name = 'test-delete'),
    path('track-user/', views.track_user, name = 'track_user'),
    path('stop-tracking/', views.stop_tracking, name = 'stop_tracking'),
    # path('',views.post_list, name='home'),
    path('',PostListView.as_view(), name='home'),
    # path('<int:pk>/<slug:slug>/', views.post_detail, name='detail'),
    path('<int:pk>/<slug:slug>/', PostDetailView.as_view(), name = 'detail'),
    path('category/<slug:slug>/',views.post_by_category,name='post_by_category'),
    path('tag/<slug:slug>/', views.post_by_tag, name = 'post_by_tag'),
    path('blog/',views.test_redirect, name = 'test_redirect'),
    path('feedback/',views.feedback, name = 'feedback'),
    # path('post/add/',views.post_add,name= 'post_add'),
    path('post/add/', PostCreateView.as_view(),name = 'post-create'),
    # path('post/update/<int:pk>/', views.post_update, name = 'post_update'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name = 'post-delete'),
    path('post/userpost/', UserPostListView.as_view(), name = 'user-post'),
    path('user/category/create/', CategoryCreateView.as_view(), name = 'category-create'),
    path('user/category/usercategory/', UserCategoryView.as_view(), name = 'user-category'),
    path('user/tag/create/', TagCreateView.as_view(), name = 'tag-create'),
    path('user/tag/usertag/', UserTagView.as_view(), name = 'user-tag'),


]