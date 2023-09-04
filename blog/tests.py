from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime, timedelta
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

class PostsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='Jawad3102')
        self.published_post = Post.objects.create(
            author=self.user,
            title='Published Post',
            text='This is a published post.',
            published_date="2023-08-17T09:39:00+08:00"
        )
        self.published_post2 = Post.objects.create(
            author=self.user,
            title='Published Post 2',
            text='This is a published post 2.',
            published_date="2023-09-25T09:39:00+08:00"
        )
        self.published_post3 = Post.objects.create(
            author=self.user,
            title='Published Post 3',
            text='This is a published post 3.',
            published_date="2023-08-21T09:39:00+08:00"
        )

        response = self.client.post('/api/auth/login', {'username': 'jawad', 'password': 'Jawad3102'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])
    
    def test_get_all_published_posts(self):
        response = self.client.get('/api/post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        responseJson = response.json()
        self.assertEqual(len(responseJson), 2)
        self.assertEqual(responseJson[0]['title'], 'Published Post')
        self.assertEqual(responseJson[0]['text'], 'This is a published post.')
        self.assertEqual(responseJson[0]['published_date'], '2023-08-17T09:39:00+08:00')

        self.assertEqual(responseJson[1]['title'], 'Published Post 3')
        self.assertEqual(responseJson[1]['text'], 'This is a published post 3.')
        self.assertEqual(responseJson[1]['published_date'], '2023-08-21T09:39:00+08:00')

        num_published_post_database = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').count()
        self.assertEqual(num_published_post_database, 2)

    def test_post_published_posts(self):
        response = self.client.get('/api/post/')
        data = {'title': 'Post 4', 
        'text': 'Post 4 Text',
        'published_date': '2023-08-31T00:00:00Z'}

        response = self.client.post('/api/post/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        responseJson = response.json()
        post_id = responseJson['id']
        submitted_post = Post.objects.filter(id=post_id)[0]

        self.assertEqual(submitted_post.title, 'Post 4')
        self.assertEqual(submitted_post.text, 'Post 4 Text')
        self.assertEqual(submitted_post.published_date.strftime('%Y-%m-%dT%H:%M:%SZ'), '2023-08-31T00:00:00Z')

class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='Jawad3102')
        self.other_user = User.objects.create_user(username='nabo', password='nabo123')
        self.published_post = Post.objects.create(
            author=self.user,
            title='Published Post',
            text='This is a published post.',
            published_date="2023-08-17T08:00:00+08:00"
        )
        response = self.client.post('/api/auth/login', {'username': 'jawad', 'password': 'Jawad3102'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_get_published_post_404(self):
        response = self.client.get(f'/api/post/545454')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_published_post(self):
        response = self.client.get(f'/api/post/{self.published_post.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['title'], 'Published Post')
        self.assertEqual(response.data['text'], 'This is a published post.')
        self.assertEqual(response.data['published_date'], "2023-08-17T08:00:00+08:00")

    def test_put_published_post(self):
        data = {'title': 'Update Test', 
        'text': 'Updating the text',
        'published_date': '2023-08-18T00:00:00Z'}
        response = self.client.put(f'/api/post/{self.published_post.id}',
         data)

        updated_post = Post.objects.filter(id=self.published_post.id)[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_post.title, 'Update Test')
        self.assertEqual(updated_post.text, 'Updating the text')
        self.assertEqual(updated_post.published_date.strftime('%Y-%m-%dT%H:%M:%SZ'), '2023-08-18T00:00:00Z')

    def test_put_published_post_404(self):
        data = {'title': 'Update Test', 
        'text': 'Updating the text',
        'published_date': '2023-08-18T09:39:00+08:00'}
        response = self.client.put(f'/api/post/5454', data)
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

    def test_delete_published_post_not_author(self):
        response = self.client.post('/api/auth/login', {'username': 'nabo', 'password': 'nabo123'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

        response = self.client.delete(f'/api/post/{self.published_post.id}')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], "You are not authorized to delete this post")

    def test_delete_published_post(self):
        response = self.client.delete(f'/api/post/{self.published_post.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check if the post has been deleted
        post_exists = Post.objects.filter(id=self.published_post.id).exists()
        self.assertFalse(post_exists)

    def test_delete_published_post_404(self):
        response = self.client.delete(f'/api/post/545454')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='Jawad3102')
        self.published_post = Post.objects.create(
            author=self.user,
            title='Published Post',
            text='This is a published post.',
            published_date="2023-08-17T08:00:00+08:00"
        )
        self.comment = Comment.objects.create(
            post=self.published_post,
            author='Nabo',
            text="HAHAHAHAH",
            approved_comment=True
        )
        self.comment2 = Comment.objects.create(
            post=self.published_post,
            author='Jawad',
            text="LMAOOOOOO",
            approved_comment=True
        )
        response = self.client.post('/api/auth/login', {'username': 'jawad', 'password': 'Jawad3102'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_get_comments_from_post_404(self):
        response = self.client.get(f'/api/post/545454/comment')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comments_from_post(self):
        response = self.client.get(f'/api/post/{self.published_post.id}/comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        responseJson = response.json()

        self.assertEqual(len(responseJson), 2)
        self.assertEqual(responseJson[0]['author'], 'Nabo')
        self.assertEqual(responseJson[0]['text'], 'HAHAHAHAH')
        self.assertEqual(responseJson[0]['approved_comment'], True)

        self.assertEqual(responseJson[1]['author'], 'Jawad')
        self.assertEqual(responseJson[1]['text'], 'LMAOOOOOO')
        self.assertEqual(responseJson[1]['approved_comment'], True)

    def test_post_comment_from_post(self):
        data = {
            "text": "testing lang",
            "author": "Jawad",
            "approved_comment": True
        }
        response = self.client.post(f'/api/post/{self.published_post.id}/comment', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        responseJson = response.json()
        list = Comment.objects.filter(pk=responseJson['id'])
        comment = list[0]
        self.assertEqual(responseJson['author'], comment.author)
        self.assertEqual(responseJson['text'], comment.text)
        self.assertEqual(responseJson['approved_comment'], comment.approved_comment)

    def test_post_comment_from_post_404(self):
        data = {
            "text": "testing lang",
            "author": "Jawad",
            "approved_comment": True
        }
        response = self.client.post(f'/api/post/54454/comment', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)