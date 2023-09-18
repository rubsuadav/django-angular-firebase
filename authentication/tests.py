from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import requests
import json
from exampleIntegrationProyectWithFirebase.utils import generate_phone_number, delete_users_collection, delete_auth_users


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @classmethod
    def tearDownClass(cls):
        delete_users_collection()
        delete_auth_users()

    def test_login_success(self):
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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        token = response.data['token'].decode()
        headers = {'Bearer': f'Bearer {token}'}
        data = {'email': mail}
        response2 = self.client.post(
            '/api/login', data=json.dumps(data), content_type='application/json', headers=headers)

        self.assertEqual(response2.data['login'], 'success')
        self.assertEqual(response2.data['user']['email'], mail)

    def test_login_missing_token(self):
        data = {'email': 'test@example.com'}
        response = self.client.post('/api/login', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token login is missing')

    def test_login_wrong_email(self):
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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        token = response.data['token'].decode()
        headers = {'Bearer': f'Bearer {token}'}
        data = {'email': 'example@example.com'}
        response2 = self.client.post(
            '/api/login', data=json.dumps(data), content_type='application/json', headers=headers)

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_success(self):
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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_email_mal_formed(self):
        fetch = requests.get('https://randomuser.me/api/')
        password = 'password'
        name = fetch.json()['results'][0]['name']['first']
        last_name = fetch.json()['results'][0]['name']['last']
        phone_number = generate_phone_number()

        response = self.client.post('/api/register', data={
            'name': name,
            'last_name': last_name,
            'email': 'asdf',
            'password': password,
            'phone_number': phone_number
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'email malformed')

    def test_register_name_less_than_3_characters(self):
        fetch = requests.get('https://randomuser.me/api/')
        mail = fetch.json()['results'][0]['email'].replace('example', 'gmail')
        password = 'password'
        last_name = fetch.json()['results'][0]['name']['last']
        phone_number = generate_phone_number()

        response = self.client.post('/api/register', data={
            'name': 'as',
            'last_name': last_name,
            'email': mail,
            'password': password,
            'phone_number': phone_number
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],
                         'name must have more than 3 characters')

    def test_register_last_name_less_than_3_characters(self):
        fetch = requests.get('https://randomuser.me/api/')
        mail = fetch.json()['results'][0]['email'].replace('example', 'gmail')
        password = 'password'
        name = fetch.json()['results'][0]['name']['first']
        phone_number = generate_phone_number()

        response = self.client.post('/api/register', data={
            'name': name,
            'last_name': 'as',
            'email': mail,
            'password': password,
            'phone_number': phone_number
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],
                         'lastName must have more than 3 characters')

    def test_register_phone_mal_formed(self):
        fetch = requests.get('https://randomuser.me/api/')
        mail = fetch.json()['results'][0]['email'].replace('example', 'gmail')
        password = 'password'
        name = fetch.json()['results'][0]['name']['first']
        last_name = fetch.json()['results'][0]['name']['last']

        response = self.client.post('/api/register', data={
            'name': name,
            'last_name': last_name,
            'email': mail,
            'password': password,
            'phone_number': 'asdf'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'phone malformed')


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_logout_success(self):
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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        token = response.data['token'].decode()
        headers = {'Bearer': f'Bearer {token}'}
        data = {'email': mail}
        response2 = self.client.post(
            '/api/login', data=json.dumps(data), content_type='application/json', headers=headers)

        self.assertEqual(response2.data['login'], 'success')
        self.assertEqual(response2.data['user']['email'], mail)

        response3 = self.client.post('/api/logout', data=data)

        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data['logout'], 'success')
