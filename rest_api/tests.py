from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from rest_api import models, views


class APITests(LiveServerTestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        models.Settings(key='test_key', value='test_value').save()
        self.admin = models.User(
            username='pkazemi3@gmail.com',
            email='pkazemi3@gmail.com',
            password='pass1234',
            first_name='Parham',
            last_name='Kazemi',
            phone='09130001122',
            institute='University of Isfahan',
            social_id='1270001122',
        )
        self.admin.save()

    def test_settings(self):
        request = self.factory.get(reverse('get_settings'))
        response = views.get_settings(request)
        self.assertIn('test_key', response.data)

    def test_signup_successful(self):
        data = {
            "email": "pkazemi3@gmail.com",
            "password": "pass1234",
            "first_name": "Parham",
            "last_name": "Kazemi",
            "phone": "09131002030",
            "institute": "University of Isfahan",
            "social_id": "12345",
        }
        request = self.factory.post(reverse('sign_up'), data)
        response = views.sign_up(request)
        self.assertEqual(response.status_code, 400, 'Repeated email checking failed')
        data['email'] = 'a@a.com'
        del data['phone']
        request = self.factory.post(reverse('sign_up'), data)
        response = views.sign_up(request)
        self.assertEqual(response.status_code, 400, 'Missing fields checking failed')
        data.update({'phone': '09131002030', 'password': '1234'})
        request = self.factory.post(reverse('sign_up'), data)
        response = views.sign_up(request)
        self.assertEqual(response.status_code, 400, 'Weak password allowed')
        data['password'] = 'pkazemi1376'
        request = self.factory.post(reverse('sign_up'), data)
        response = views.sign_up(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.User.objects.filter(username='a@a.com').count(), 1)

    def test_login(self):
        data = {'email': 'test@test.com', 'password': 'pass1234'}
        request = self.factory.post(reverse('sign_in'), data)
        response = views.sign_in(request)
        self.assertEqual(response.status_code, 400)
        data = {'email': 'pkazemi3@gmail.com', 'password': 'wrongpassword1234'}
        request = self.factory.post(reverse('sign_in'), data)
        response = views.sign_in(request)
        self.assertEqual(response.status_code, 400)
        data = {'email': self.admin.username, 'password': self.admin.password}
        request = self.factory.post(reverse('sign_in'), data)
        response = views.sign_in(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)
