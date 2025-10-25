# In django_frontend/frontend_config/urls.py

from django.contrib import admin
from django.urls import path, include # Make sure 'include' is imported

urlpatterns = [
    # Django admin site (optional for the frontend project, but doesn't hurt)
    path('admin/', admin.site.urls),

    # Include all URLs defined in the 'pages' app's urls.py file
    # Any request that doesn't match '/admin/' will be sent here.
    path('', include('pages.urls')),
]

# Note: We don't need static/media file serving here unless your
# frontend templates specifically use Django's staticfiles app.
# Your CSS is likely served directly by the http.server.