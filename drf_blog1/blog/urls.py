from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for potential ViewSet expansion

urlpatterns = [
    
    # Post URLs
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:id>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:id>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:id>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
    # Additional endpoints
    path('recent-posts/', views.recent_posts, name='recent-posts'),
    
    # Authentication URLs
    path('auth/test/', views.test_auth, name='test-auth'),
    path('auth/register/', views.user_registration, name='user-registration'),
    path('auth/login/', views.user_login, name='user-login'),
    path('auth/logout/', views.user_logout, name='user-logout'),
    path('auth/profile/', views.user_profile, name='user-profile'),
    path('auth/profile/update/', views.update_user_profile, name='update-user-profile'),
]