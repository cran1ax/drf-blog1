# Update blog/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post
from django.utils import timezone

class BlogAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.user,
        )
    
    def test_post_list(self):
        url = reverse('post-list')
        response = self.client.get(url)
        print(f"Post list URL: {url}")
        print(f"Post list status: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: response.data might be paginated, so we check the count
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)
    
    def test_post_detail(self):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')

class ModelTests(TestCase):
    def test_post_creation(self):
        user = User.objects.create_user(username='modeluser', password='test123')
        post = Post.objects.create(
            title='Model Test Post',
            content='Test content',
            author=user,
        )
        self.assertEqual(str(post), 'Model Test Post')
