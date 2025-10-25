from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Post
# Removed template-specific imports
from .serializers import (
    PostListSerializer,
    PostDetailSerializer, PostCreateSerializer,
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer
)

# ===================================================================
# API VIEWS
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
    permission_classes = [permissions.IsAuthenticated] # Requires JWT token

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def recent_posts(request):
    posts = Post.objects.all().order_by('-created_at')[:5]
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)

# API endpoint for registration
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully via API',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API endpoint to get user profile (requires token)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated]) # Requires JWT token
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# API endpoint to update user profile (requires token)
@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated]) # Requires JWT token
def update_user_profile(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully via API',
            'user': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated] # Requires JWT token
    lookup_field = 'id'

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.IsAuthenticated] # Requires JWT token
    lookup_field = 'id'

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to delete this post.")
        instance.delete()

# ALL TEMPLATE VIEWS (def home, def login_view, etc.) ARE REMOVED