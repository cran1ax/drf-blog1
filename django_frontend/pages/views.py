# In django_frontend/pages/views.py

from django.shortcuts import render
import requests # Make sure you installed this!

# Define the base URL of your backend API
BACKEND_API_URL = 'http://127.0.0.1:8000/api' # No trailing slash

def home(request):
    """
    Fetches recent posts from the backend API and renders the homepage.
    """
    error = None
    recent_posts_data = [] # Default to an empty list

    try:
        # 1. Make a GET request to the backend API's recent posts endpoint
        api_url = f"{BACKEND_API_URL}/recent-posts/"
        response = requests.get(api_url)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # 2. Parse the JSON response
        recent_posts_data = response.json()

    except requests.exceptions.RequestException as e:
        # Handle errors (API server down, network issues, invalid JSON)
        error = f"Could not fetch recent posts from API: {e}"
        print(f"API Error: {e}") # Log the error for debugging

    # 3. Prepare the context for the template
    context = {
        'recent_posts': recent_posts_data,
        'api_error': error # Pass the error message to the template
    }

    # 4. Render the index.html template
    return render(request, 'index.html', context)


def all_posts(request):
    """
    Fetches all posts from the backend API and renders the all_posts page.
    """
    error = None
    posts_data = [] # Default to an empty list

    try:
        # 1. Make a GET request to the backend API's posts list endpoint
        api_url = f"{BACKEND_API_URL}/posts/"
        response = requests.get(api_url)
        response.raise_for_status()

        # 2. Parse the JSON response
        data = response.json()
        # Handle potential pagination from DRF
        posts_data = data.get('results', data) if isinstance(data, dict) else data


    except requests.exceptions.RequestException as e:
        error = f"Could not fetch posts from API: {e}"
        print(f"API Error: {e}")

    # 3. Prepare the context
    context = {
        'posts': posts_data,
        'api_error': error
    }

    # 4. Render the all_posts.html template
    return render(request, 'all_posts.html', context)


def post_detail(request, post_id):
    """
    Fetches a single post from the backend API and renders its detail page.
    """
    error = None
    post_data = None # Default to None

    try:
        # 1. Make a GET request to the backend API's post detail endpoint
        api_url = f"{BACKEND_API_URL}/posts/{post_id}/"
        response = requests.get(api_url)
        response.raise_for_status() # Will raise HTTPError for 404

        # 2. Parse the JSON response
        post_data = response.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            error = "Post not found."
        else:
            error = f"Could not fetch post detail from API: {e}"
        print(f"API Error: {e}")
    except requests.exceptions.RequestException as e:
        error = f"Could not fetch post detail from API: {e}"
        print(f"API Error: {e}")

    # 3. Prepare the context
    context = {
        'post': post_data,
        'api_error': error
    }

    # 4. Render the post_detail.html template
    return render(request, 'post_detail.html', context)

# --- Views requiring Authentication (Login, Register, Create, Update, Delete, Profile) ---
# These are more complex because they involve:
# 1. Handling HTML form submissions (POST requests).
# 2. Making POST/PUT/DELETE requests to the backend API.
# 3. Handling API authentication (sending JWT tokens).
# 4. Storing the JWT token (e.g., in the Django session on the *frontend* server).
# 5. Redirecting the user.
# We can add these next if you want. Let's get the read-only pages working first.