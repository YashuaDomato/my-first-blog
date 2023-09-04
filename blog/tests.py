from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .models import Post, Comment
# Create your tests here.
class CustomAuthTokenTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='Jawad3102')

    def test_custom_auth_token_valid(self):
        response = self.client.post('/api/auth/login', {'username': 'jawad', 'password': 'Jawad3102'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        token = response.data['token']

    def test_custom_auth_token_fail(self):
        response = self.client.post('/api/auth/login', {'username': 'jawad45', 'password': '3213'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid username/password')

class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='Jawad3102')
        self.other_user = User.objects.create_user(username='nabo', password='nabo123')
        self.published_post = Post.objects.create(
            author=self.user,
            title='Published Post',
            text='This is a published post.',
            published_date="2023-08-17T09:39:00+08:00"
        )
        response = self.client.post('/api/auth/login', {'username': 'jawad', 'password': 'Jawad3102'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_get_published_post(self):
        response = self.client.get(f'/api/post/{self.published_post.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Published Post')
        self.assertEqual(response.data['text'], 'This is a published post.')
        self.assertEqual(response.data['published_date'], '2023-08-17T09:39:00+08:00')

    def test_get_published_post_404(self):
        response = self.client.get(f'/api/post/545454')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_published_post(self):
        data = {'title': 'Update Test', 
        'text': 'Updating the text',
        'published_date': '2023-08-18T09:39:00+08:00'}
        response = self.client.put(f'/api/post/{self.published_post.id}',
         data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Update Test')
        self.assertEqual(response.data['text'], 'Updating the text')
        self.assertEqual(response.data['published_date'], '2023-08-18T09:39:00+08:00')

    def test_put_published_post_404(self):
        data = {'title': 'Update Test', 
        'text': 'Updating the text',
        'published_date': '2023-08-18T09:39:00+08:00'}
        response = self.client.put(f'/api/post/5454',
         data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_published_post_not_author(self):
        response = self.client.post('/api/auth/login', {'username': 'nabo', 'password': 'nabo123'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])
        data = {'title': 'Update Test', 
        'text': 'Updating the text',
        'published_date': '2023-08-18T09:39:00+08:00'}
        response = self.client.put(f'/api/post/{self.published_post.id}',
         data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], "You are not authorized to edit this post")