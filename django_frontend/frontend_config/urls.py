# In django_frontend/frontend_config/urls.py

from django.urls import path, include

# Import all views from the pages app
from pages import views as page_views

urlpatterns = [

    # --- Frontend Page URLs ---
    path('', page_views.home, name='home'),
    path('posts/', page_views.all_posts, name='all_posts'),
    path('posts/<int:post_id>/', page_views.post_detail, name='post_detail'),
    path('login/', page_views.login_view, name='login'),
    path('register/', page_views.register_view, name='register'),
    path('logout/', page_views.logout_view, name='logout'),
    path('profile/', page_views.profile_view, name='profile'),
    path('create-post/', page_views.create_post_view, name='create_post'),
    path('posts/<int:post_id>/update/', page_views.update_post_view, name='update_post'), 
    path('posts/<int:post_id>/delete/', page_views.delete_post_view, name='delete_post'),
]

# Note: We are defining all page URLs here directly.
# The include('pages.urls') line is removed.