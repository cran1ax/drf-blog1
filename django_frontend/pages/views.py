# In django_frontend/pages/views.py

from django.shortcuts import render, redirect
import requests

# Define the base URL of your backend API
BACKEND_API_URL = 'http://127.0.0.1:8001/api' # Port 8001 for backend

# --- Helper function to check auth status ---
def is_authenticated(request):
    return 'access_token' in request.session

# --- Page Views ---

# --- Update Post View ---
def update_post_view(request, post_id):
    """
    Renders and handles the 'update_post.html' form.
    Submits updated data to the backend API.
    """
    if not is_authenticated(request):
        return redirect('login')

    error = None
    errors_dict = None
    post_data = None
    access_token = request.session.get('access_token')
    api_url_detail = f"{BACKEND_API_URL}/posts/{post_id}/"
    headers = {'Authorization': f'Bearer {access_token}'}

    # --- Handle POST request (Form Submission) ---
    if request.method == 'POST':
        try:
            update_data = {
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
            }
            api_url_update = f"{BACKEND_API_URL}/posts/{post_id}/update/"
            response = requests.put(api_url_update, headers=headers, data=update_data) # Use PUT
            response.raise_for_status()

            # Success! Redirect back to the post detail page
            return redirect('post_detail', post_id=post_id)

        except requests.exceptions.HTTPError as e:
             if e.response.status_code == 400: errors_dict = e.response.json()
             elif e.response.status_code in [401, 403]: errors_dict = {'auth_error': ['Update failed. Check permissions or log in again.']}
             else: errors_dict = {'api_error': [f"API Error ({e.response.status_code}): {e.response.text}"]}
             print(f"API Update Post Error ({e.response.status_code}): {e}")
             # Re-render form with errors, use POST data for field values
             post_data = request.POST # Show submitted data
        except requests.exceptions.RequestException as e:
            error = f"Could not connect to update post API: {e}"
            print(f"API Update Post Connection Error: {e}")
            # Fall through to GET logic to fetch original post data

    # --- Handle GET request (Show Form) or Re-render after POST error ---
    # Fetch original post data if not already fetched or if POST failed without specific field errors
    if not post_data or error:
        try:
            response = requests.get(api_url_detail, headers=headers) # Fetch needed even for POST error display
            response.raise_for_status()
            fetched_post_data = response.json()
            # If re-rendering after POST error, keep submitted data, else use fetched data
            if not post_data:
                post_data = fetched_post_data

        except requests.exceptions.RequestException as e:
            error = f"Could not fetch post to update from API: {e}"
            print(f"API Update Post Fetch Error: {e}")
            if e.response and e.response.status_code == 401:
                 if 'access_token' in request.session: del request.session['access_token']
                 return redirect('login')

    context = {
        'post': post_data, # Contains either fetched data or failed POST data
        'api_error': error,
        'errors': errors_dict,
        'user_is_authenticated': True,
        'post_id': post_id # Pass post_id for form action URL
    }
    return render(request, 'update_post.html', context)


# --- Delete Post View ---
def delete_post_view(request, post_id):
    """
    Renders confirmation page and handles post deletion via backend API.
    """
    if not is_authenticated(request):
        return redirect('login')

    error = None
    post_data = None
    access_token = request.session.get('access_token')
    api_url = f"{BACKEND_API_URL}/posts/{post_id}/"
    headers = {'Authorization': f'Bearer {access_token}'}

    # --- Handle POST request (Confirmation) ---
    if request.method == 'POST':
        try:
            api_url_delete = f"{BACKEND_API_URL}/posts/{post_id}/delete/"
            response = requests.delete(api_url_delete, headers=headers)
            response.raise_for_status() # Check for errors (401, 403, 404, 500)

            # Success! Redirect to the list of all posts
            return redirect('all_posts')

        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [401, 403]: error = "Delete failed. Check permissions or log in again."
            elif e.response.status_code == 404: error = "Post not found."
            else: error = f"API Error during delete ({e.response.status_code}): {e.response.text}"
            print(f"API Delete Post Error ({e.response.status_code}): {e}")
            # Fall through to re-render confirmation page with error
        except requests.exceptions.RequestException as e:
            error = f"Could not connect to delete post API: {e}"
            print(f"API Delete Post Connection Error: {e}")
            # Fall through to re-render confirmation page with error

    # --- Handle GET request (Show Confirmation) or Re-render after POST error ---
    # Fetch post data to display confirmation details
    if not post_data: # Only fetch if not re-rendering after POST error
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            post_data = response.json()
        except requests.exceptions.RequestException as e:
            # If fetching fails, show error but maybe still allow delete attempt
            fetch_error = f"Could not fetch post details from API: {e}"
            print(f"API Delete Post Fetch Error: {e}")
            if e.response and e.response.status_code == 401:
                if 'access_token' in request.session: del request.session['access_token']
                return redirect('login')
            if not error: error = fetch_error # Show fetch error if no delete error occurred

    context = {
        'post': post_data,
        'api_error': error,
        'user_is_authenticated': True,
        'post_id': post_id
    }
    return render(request, 'delete_post.html', context)
# --- Create Post View ---
def create_post_view(request):
    """
    Renders and handles the 'create_post.html' form.
    Submits data to the backend API.
    """
    if not is_authenticated(request):
        return redirect('login') # Must be logged in

    errors = None
    access_token = request.session.get('access_token')

    if request.method == 'POST':
        try:
            post_data = {
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                # Add 'featured_image' if your form supports it
            }
            api_url = f"{BACKEND_API_URL}/posts/create/"
            headers = {'Authorization': f'Bearer {access_token}'}

            response = requests.post(api_url, headers=headers, data=post_data)
            response.raise_for_status() # Check for errors

            # Success! Get the ID of the newly created post from the API response
            new_post_data = response.json()
            new_post_id = new_post_data.get('id')
            if new_post_id:
                return redirect('post_detail', post_id=new_post_id) # Redirect to the new post
            else:
                return redirect('all_posts') # Fallback redirect

        except requests.exceptions.HTTPError as e:
             if e.response.status_code == 400: errors = e.response.json() # Validation errors
             elif e.response.status_code in [401, 403]: errors = {'auth_error': ['Authentication failed or forbidden. Please log in again.']}
             else: errors = {'api_error': [f"API Error ({e.response.status_code}): {e.response.text}"]}
             print(f"API Create Post Error ({e.response.status_code}): {e}")
        except requests.exceptions.RequestException as e:
            errors = {'connection_error': [f"Could not connect to create post API: {e}"]}
            print(f"API Create Post Connection Error: {e}")

        # Re-render form with errors if POST failed
        context = {'errors': errors, 'user_is_authenticated': True, 'submitted_data': request.POST}
        return render(request, 'create_post.html', context)

    else: # GET request
        context = {'user_is_authenticated': True}
        return render(request, 'create_post.html', context)
def profile_view(request):
    """
    Fetches user profile from backend API and renders profile page.
    Redirects to login if not authenticated.
    """
    if not is_authenticated(request):
        return redirect('login') # Redirect to login if no token

    error = None
    profile_data = None
    access_token = request.session.get('access_token')

    # Handle profile update form submission
    if request.method == 'POST':
        try:
            update_data = {
                'first_name': request.POST.get('first_name', ''),
                'last_name': request.POST.get('last_name', ''),
                'email': request.POST.get('email', '')
            }
            api_url = f"{BACKEND_API_URL}/auth/profile/update/"
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.put(api_url, headers=headers, data=update_data) # Use PUT or PATCH
            response.raise_for_status()
            # Successfully updated, redirect back to profile page to show changes
            return redirect('profile')

        except requests.exceptions.HTTPError as e:
             if e.response.status_code == 400: errors_dict = e.response.json()
             else: errors_dict = {'api_error': [f"API Error ({e.response.status_code}): {e.response.text}"]}
             print(f"API Profile Update Error ({e.response.status_code}): {e}")
             # Re-render form with errors
             profile_data = request.POST # Show submitted data again
             context = {'profile': profile_data, 'errors': errors_dict, 'user_is_authenticated': True}
             return render(request, 'profile.html', context)
        except requests.exceptions.RequestException as e:
            error = f"Could not connect to update profile API: {e}"
            print(f"API Profile Update Connection Error: {e}")
            # Fall through to render profile page with connection error

    # Fetch profile data for GET request or after failed POST
    if not profile_data: # Only fetch if not re-rendering after failed POST
        try:
            api_url = f"{BACKEND_API_URL}/auth/profile/"
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            profile_data = response.json()

        except requests.exceptions.RequestException as e:
            error = f"Could not fetch profile from API: {e}"
            print(f"API Profile Fetch Error: {e}")
            if e.response and e.response.status_code == 401: # Handle expired/invalid token
                 # Clear session and redirect to login
                 if 'access_token' in request.session: del request.session['access_token']
                 if 'refresh_token' in request.session: del request.session['refresh_token']
                 return redirect('login')

    context = {
        'profile': profile_data, # This will be the user data dict from API
        'api_error': error,
        'user_is_authenticated': True
    }
    return render(request, 'profile.html', context)

def home(request):
    error = None
    recent_posts_data = []
    try:
        api_url = f"{BACKEND_API_URL}/recent-posts/"
        response = requests.get(api_url)
        response.raise_for_status()
        recent_posts_data = response.json()
    except requests.exceptions.RequestException as e:
        error = f"Could not fetch recent posts from API: {e}"
        print(f"API Error (home): {e}")

    context = {
        'recent_posts': recent_posts_data,
        'api_error': error,
        'user_is_authenticated': is_authenticated(request) # Pass auth status to template
    }
    return render(request, 'index.html', context)

def all_posts(request):
    error = None
    posts_data = []
    try:
        api_url = f"{BACKEND_API_URL}/posts/"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        posts_data = data.get('results', data) if isinstance(data, dict) else data
    except requests.exceptions.RequestException as e:
        error = f"Could not fetch posts from API: {e}"
        print(f"API Error (all_posts): {e}")

    context = {
        'posts': posts_data,
        'api_error': error,
        'user_is_authenticated': is_authenticated(request)
    }
    return render(request, 'all_posts.html', context)

def post_detail(request, post_id):
    error = None
    post_data = None
    try:
        api_url = f"{BACKEND_API_URL}/posts/{post_id}/"
        response = requests.get(api_url)
        response.raise_for_status()
        post_data = response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404: error = "Post not found."
        else: error = f"Could not fetch post detail from API: {e}"
        print(f"API Error (post_detail 404/500): {e}")
    except requests.exceptions.RequestException as e:
        error = f"Could not fetch post detail from API: {e}"
        print(f"API Error (post_detail other): {e}")

    context = {
        'post': post_data,
        'api_error': error,
        'user_is_authenticated': is_authenticated(request)
    }
    return render(request, 'post_detail.html', context)

# --- Authentication Views ---

def login_view(request):
    """
    Renders login form & handles login via backend API token endpoint.
    Stores the received token in the frontend's session.
    """
    if is_authenticated(request): # Check session for token
         return redirect('home')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Call the backend API's token endpoint
            # Note: Need to adjust URL base if BACKEND_API_URL includes /api
            api_token_url = f"{BACKEND_API_URL.replace('/api', '')}/api/token/"
            response = requests.post(api_token_url, data={'username': username, 'password': password})
            response.raise_for_status()

            token_data = response.json()
            access_token = token_data.get('access')
            refresh_token = token_data.get('refresh') # Optional: store refresh token too

            if access_token:
                # SUCCESS: Store token in frontend session
                request.session['access_token'] = access_token
                # request.session['refresh_token'] = refresh_token # Store refresh if needed
                request.session.set_expiry(0) # Make session last until browser closes
                print("Token stored in session")
                return redirect('home')
            else:
                error = "Login failed: No token received from API."

        except requests.exceptions.HTTPError as e:
             if e.response.status_code == 401: error = "Invalid username or password."
             else: error = f"API Error during login ({e.response.status_code}): {e.response.text}"
             print(f"API Login Error ({e.response.status_code}): {e}")
        except requests.exceptions.RequestException as e:
            error = f"Could not connect to login API: {e}"
            print(f"API Login Connection Error: {e}")

    context = {'error': error, 'user_is_authenticated': False}
    return render(request, 'login.html', context)

def register_view(request):
    """
    Renders registration form & handles registration via backend API.
    """
    if is_authenticated(request):
         return redirect('home')

    errors = None
    if request.method == 'POST':
        data_to_send = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', '')
        }
        try:
            api_url = f"{BACKEND_API_URL}/auth/register/"
            response = requests.post(api_url, data=data_to_send)
            response.raise_for_status()

            # SUCCESS: Redirect to login page
            return redirect('login')

        except requests.exceptions.HTTPError as e:
             if e.response.status_code == 400: errors = e.response.json()
             else: errors = {'api_error': [f"API Error ({e.response.status_code}): {e.response.text}"]}
             print(f"API Registration Error ({e.response.status_code}): {e}")
             print("API Response:", e.response.text)
        except requests.exceptions.RequestException as e:
            errors = {'connection_error': [f"Could not connect to registration API: {e}"]}
            print(f"API Registration Connection Error: {e}")

    context = {'errors': errors, 'user_is_authenticated': False}
    return render(request, 'register.html', context)

def logout_view(request):
    """
    Logs the user out by clearing the token from the frontend session.
    """
    if 'access_token' in request.session:
        del request.session['access_token']
    if 'refresh_token' in request.session:
        del request.session['refresh_token']
    print("Token removed from session")
    return redirect('home')

# --- TODO: Add create_post_view, profile_view, update_post_view, delete_post_view ---
# These will need to:
# 1. Check if 'access_token' is in request.session. If not, redirect to login.
# 2. Include the token in the 'Authorization: Bearer <token>' header when calling the backend API.
# Example: headers={'Authorization': f'Bearer {request.session["access_token"]}'}