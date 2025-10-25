from django.urls import path, include
# Removed DefaultRouter import as it wasn't used
from . import views

urlpatterns = [

    # Post API URLs
    path('posts/', views.PostListView.as_view(), name='post-list-api'),
    path('posts/create/', views.PostCreateView.as_view(), name='post-create-api'),
    path('posts/<int:id>/', views.PostDetailViewAPI.as_view(), name='post-detail-api'),
    path('posts/<int:id>/update/', views.PostUpdateView.as_view(), name='post-update-api'),
    path('posts/<int:id>/delete/', views.PostDeleteView.as_view(), name='post-delete-api'),

    # Additional Post API endpoints
    path('recent-posts/', views.recent_posts, name='recent-posts-api'),

    # Authentication API URLs
    path('auth/register/', views.user_registration, name='register-api'),
    # JWT login/logout handled in project urls.py
    path('auth/profile/', views.user_profile, name='profile-api'),
    path('auth/profile/update/', views.update_user_profile, name='update-profile-api'),
]