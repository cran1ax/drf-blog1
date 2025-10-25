# In django_frontend/pages/urls.py

from django.urls import path
from . import views # Import views from the current app (pages)

# This defines the URL patterns for the 'pages' app
urlpatterns = [
    # Example: Map the root URL ('/') of this app to the 'home' view
    path('', views.home, name='home'),

    # Map '/posts/' to the 'all_posts' view
    path('posts/', views.all_posts, name='all_posts'),

    # Map '/posts/<some_integer>/' to the 'post_detail' view
    # The <int:post_id> part captures the integer from the URL
    # and passes it as an argument to the view function.
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),

    # We will add URLs for login, register, profile, create, etc. later
]