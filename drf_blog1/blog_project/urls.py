from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 1. Import all your template views
from blog.views import (
    home, 
    all_posts, 
    login_view, 
    register_view, 
    logout_view,
    post_detail,
    create_post_view,
    profile_view,
    update_post_view,  
    delete_post_view
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- API URLS (These still work) ---
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('blog.urls')),

    # --- FRONTEND (TEMPLATE) URLS ---
    path('', home, name='home'), 
    path('posts/', all_posts, name='all_posts'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('create-post/', create_post_view, name='create_post'),
    path('posts/<int:post_id>/update/', update_post_view, name='update_post'),
    path('posts/<int:post_id>/delete/', delete_post_view, name='delete_post'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)