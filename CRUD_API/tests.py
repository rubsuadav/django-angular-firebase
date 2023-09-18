from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import requests
from authentication.tests import generate_phone_number
import json
from firebase_admin import firestore


def get_token(self):
    fetch = requests.get('https://randomuser.me/api/')
    mail = fetch.json()['results'][0]['email'].replace('example', 'gmail')
    password = 'password'
    name = fetch.json()['results'][0]['name']['first']
    last_name = fetch.json()['results'][0]['name']['last']
    phone_number = generate_phone_number()
    response = self.client.post('/api/register', data={
        'name': name,
        'last_name': last_name,
        'email': mail,
        'password': password,
        'phone_number': phone_number
    })

    return response.data['token'].decode()


class PostListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    ######################################################## GETS #######################################################

    def test_get_all_posts(self):
        response = self.client.get('/api/post')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_post(self):
        response = self.client.get('/api/post/p6pCJAOItxbOJT9gMl6V')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'titulo 1')

    def test_get_nonexistent_post(self):
        response = self.client.get('/api/post/999')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Post not found')

    ######################################################## POSTS #######################################################

    def test_create_post(self):
        headers = {'Bearer': f'Bearer {get_token(self)}'}
        data = {'title': 'Test Post', 'content': 'This is a test post.'}

        response = self.client.post(
            '/api/post', data=json.dumps(data), content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_missing_token(self):
        data = {'title': 'Test Post', 'content': 'This is a test post.'}
        response = self.client.post(
            '/api/post', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token login is missing')

    def test_create_post_invalid_title(self):
        headers = {'Bearer': f'Bearer {get_token(self)}'}
        data = {'title': '', 'content': 'This is a test post.'}
        response = self.client.post(
            '/api/post', data=json.dumps(data), content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],
                         'title must have more than 3 characters')

    def test_create_post_invalid_content(self):
        headers = {'Bearer': f'Bearer {get_token(self)}'}
        data = {'title': 'Test Post', 'content': ''}
        response = self.client.post(
            '/api/post', data=json.dumps(data), content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],
                         'content must have more than 3 characters')

    ######################################################## PUTS #######################################################

    def test_update_post(self):
        firestore.client().collection(u'posts').document().create({
            u'title': 'Test 2 Post',
            u'content': 'This is a test 2 post.'
        })
        uid = firestore.client().collection(u'posts')._query().where(
            u'title', u'==', u'Test 2 Post').get()[0].id
        headers = {'Bearer': f'Bearer {get_token(self)}'}
        data = {'title': 'Test 2 Post updated',
                'content': 'This is a test 2 post'}
        response = self.client.put(
            f'/api/post/{uid}', data=json.dumps(data), content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Post updated')

    def test_update_nonexistent_post(self):
        headers = {'Bearer': f'Bearer {get_token(self)}'}
        data = {'title': 'Test 2 Post updated',
                'content': 'This is a test 2 post'}
        response = self.client.put(
            '/api/post/999', data=json.dumps(data), content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Post not found')

    def test_update_post_missing_token(self):
        data = {'title': 'Test 2 Post updated',
                'content': 'This is a test 2 post'}
        response = self.client.put(
            '/api/post/12', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token login is missing')

    def test_update_post_invalid_title(self):
        uid = firestore.client().collection(u'posts')._query().where(
            u'title', u'==', u'Test 2 Post updated').get()[0].id
        headers = {'Bearer': f'Bearer {get_token(self)}'}
        data = {'title': '',
                'content': 'This is a test 2 post'}
        response = self.client.put(
            f'/api/post/{uid}', data=json.dumps(data), content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],
                         'title must have more than 3 characters')

    def test_update_post_invalid_content(self):
        uid = firestore.client().collection(u'posts')._query().where(
            u'title', u'==', u'Test 2 Post updated').get()[0].id
        headers = {'Bearer': f'Bearer {get_token(self)}'}
        data = {'title': 'Test 2 Post updated',
                'content': ''}
        response = self.client.put(
            f'/api/post/{uid}', data=json.dumps(data), content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],
                         'content must have more than 3 characters')

    ######################################################## DELETES #######################################################

    def test_delete_post(self):
        firestore.client().collection(u'posts').document().create({
            u'title': 'Test 3 Post',
            u'content': 'This is a test 3 post.'
        })
        uid = firestore.client().collection(u'posts')._query().where(
            u'title', u'==', u'Test 3 Post').get()[0].id
        headers = {'Bearer': f'Bearer {get_token(self)}'}
        response = self.client.delete(f'/api/post/{uid}', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Post deleted')

    def test_delete_nonexistent_post(self):
        headers = {'Bearer': f'Bearer {get_token(self)}'}
        response = self.client.delete('/api/post/999',  headers=headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Post not found')

    def test_delete_post_missing_token(self):
        response = self.client.delete('/api/post/jSYfgxX5ok8K69fSn6dq')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token login is missing')
