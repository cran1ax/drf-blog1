from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Post
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .serializers import (
    PostListSerializer, 
    PostDetailSerializer, PostCreateSerializer,
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer
)

# ===================================================================
# API VIEWS (For your old React app / external apps)
# ===================================================================

class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Post.objects.all().select_related('author')
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        return queryset

class PostDetailViewAPI(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'
    queryset = Post.objects.all()

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def recent_posts(request):
    posts = Post.objects.all().order_by('-created_at')[:5]
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User created successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_user_profile(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to delete this post.")
        instance.delete()

# ===================================================================
# TRADITIONAL (TEMPLATE) VIEWS (For your new frontend)
# ===================================================================

def home(request):
    """
    Renders the homepage (index.html).
    """
    recent_posts = Post.objects.all().order_by('-created_at')[:5]
    context = {
        'recent_posts': recent_posts
    }
    return render(request, 'index.html', context)

def all_posts(request):
    """
    Renders the 'all_posts.html' page.
    """
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'all_posts.html', context)

def post_detail(request, post_id):
    """
    Renders the 'post_detail.html' page for a single post.
    """
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post
    }
    return render(request, 'post_detail.html', context)

def login_view(request):
    """
    Handles user login.
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            context = {'error': 'Invalid username or password.'}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

def register_view(request):
    """
    Handles user registration.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # We re-use the API serializer!
        serializer = UserRegistrationSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')
        else:
            context = {'errors': serializer.errors}
            return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')

def logout_view(request):
    """
    Logs the user out and redirects to home.
    """
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile_view(request):
    """
    Renders the 'profile.html' page.
    """
    # This is a protected view. @login_required decorator
    # will redirect to /login/ if the user is not logged in.
    
    # We re-use the API serializer here too
    if request.method == 'POST':
        # Handle profile update
        serializer = UserSerializer(request.user, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return redirect('profile')
        else:
            context = {'errors': serializer.errors}
            return render(request, 'profile.html', context)
    else:
        # Just show the profile
        return render(request, 'profile.html')

@login_required(login_url='login')
def create_post_view(request):
    """
    Renders and handles the 'create_post.html' form.
    """
    if request.method == 'POST':
        # We re-use the API serializer!
        # We must add the author (the logged-in user)
        data = request.POST.copy()
        data['author'] = request.user
        
        serializer = PostCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save(author=request.user)
            return redirect('post_detail', post_id=post.id)
        else:
            context = {'errors': serializer.errors}
            return render(request, 'create_post.html', context)
    else:
        return render(request, 'create_post.html')
    
@login_required(login_url='login')
def update_post_view(request, post_id):
    """
    Renders and handles the 'update_post.html' form.
    """
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the logged-in user is the author
    if post.author != request.user:
        return redirect('home') # Or show a 'permission denied' error

    if request.method == 'POST':
        # We pass 'instance=post' to update the existing post
        serializer = PostCreateSerializer(instance=post, data=request.POST, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return redirect('post_detail', post_id=post.id)
        else:
            context = {'errors': serializer.errors, 'post': post}
            return render(request, 'update_post.html', context)
    else:
        # Show the form pre-filled with the existing post data
        context = {'post': post}
        return render(request, 'update_post.html', context)

@login_required(login_url='login')
def delete_post_view(request, post_id):
    """
    Renders a confirmation page and handles post deletion.
    """
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the logged-in user is the author
    if post.author != request.user:
        return redirect('home') # Or show a 'permission denied' error

    if request.method == 'POST':
        # This is the confirmation step
        post.delete()
        return redirect('all_posts') # Redirect to the 'all posts' page
    else:
        # Show the confirmation page
        context = {'post': post}
        return render(request, 'delete_post.html', context)