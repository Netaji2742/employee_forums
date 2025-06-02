from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post, Connection

class UserAuthTests(APITestCase):
    def test_user_registration(self):
        url = '/api/register/'
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login(self):
        User.objects.create_user(username='testuser', password='testpass123')
        url = '/api/login/'
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class PostTests(APITestCase):
    def setUp(self):
        '''''
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpass123'}).data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        '''
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        login_response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpass123'})
        print("Login response:", login_response.data)
        self.token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        
    def test_create_post(self):
        response = self.client.post('/api/posts/create/', {'content': 'Hello World!'})
        print("Create Post Response:", response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Hello World!')

    def test_like_and_unlike_post(self):
        post_response = self.client.post('/api/posts/create/', {'content': 'Test Post'})
        print("Post Creation Status:", post_response.status_code)
        print("Post Creation Content:", post_response.content)

        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        post_id = post_response.data['id']

        like_response = self.client.post(f'/api/posts/{post_id}/like/')
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)

        unlike_response = self.client.post(f'/api/posts/{post_id}/unlike/')
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)

class ConnectionTests(APITestCase):
    def setUp(self):
        '''''
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.token1 = self.client.post('/api/login/', {'username': 'user1', 'password': 'pass1'}).data['token']
        self.token2 = self.client.post('/api/login/', {'username': 'user2', 'password': 'pass2'}).data['token']
        '''
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        login1 = self.client.post('/api/login/', {'username': 'user1', 'password': 'pass1'})
        self.token1 = login1.data['token']
        login2 = self.client.post('/api/login/', {'username': 'user2', 'password': 'pass2'})
        self.token2 = login2.data['token']

    def test_send_and_accept_connection(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        send_response = self.client.post(f'/api/connections/send/{self.user2.id}/')
        self.assertEqual(send_response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        requests_response = self.client.get('/api/connections/requests/')
        self.assertEqual(requests_response.status_code, status.HTTP_200_OK)
        conn_id = requests_response.data[0]['id']

        accept_response = self.client.post(f'/api/connections/accept/{conn_id}/')
        self.assertEqual(accept_response.status_code, status.HTTP_200_OK)
