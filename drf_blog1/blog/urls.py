from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for potential ViewSet expansion

urlpatterns = [
    
    # Post URLs
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post-create-api'),
    
    # This line is changed to point to the renamed API view
    path('posts/<int:id>/', views.PostDetailViewAPI.as_view(), name='post-detail-api'), 
    
    path('posts/<int:id>/update/', views.PostUpdateView.as_view(), name='post-update-api'),
    path('posts/<int:id>/delete/', views.PostDeleteView.as_view(), name='post-delete-api'),
    
    # Additional endpoints
    path('recent-posts/', views.recent_posts, name='recent-posts-api'),
    
    # Authentication URLs
    path('auth/register/', views.user_registration, name='register-api'),
    
    # We no longer need these as they are handled by simplejwt
    # path('auth/login/', views.user_login, name='login-api'),
    # path('auth/logout/', views.user_logout, name='logout-api'),
    
    path('auth/profile/', views.user_profile, name='profile-api'),
    path('auth/profile/update/', views.update_user_profile, name='update-profile-api'),
]