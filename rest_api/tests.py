from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from rest_api import models, views


class APITests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        models.Settings(key='test_key', value='test_value').save()
        self.test_user1 = models.User.objects.create_user(
            email='pkazemi3@gmail.com',
            password='pkazemi1376',
            first_name='Parham',
            last_name='Kazemi',
            phone='09130001122',
            institute='University of Isfahan',
            social_id='1270001122',
        )
        self.test_user2 = models.User.objects.create_user(
            email='pkazemi76@yahoo.com',
            password='pkazemi1376',
            first_name='Test',
            last_name='User',
            phone='09139998877',
            institute='University of Isfahan',
            social_id='1279998877',
        )

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
        self.assertEqual(models.User.objects.filter(email='a@a.com').count(), 1, 'User object not created')

    def test_edit_and_get_user_info(self):
        data = self.test_user1.get_dict()
        data['phone'] = '09130001122'
        request = self.factory.post(reverse('edit_user_info'), data)
        force_authenticate(request, self.test_user1)
        response = views.edit_user_info(request)
        self.assertEqual(response.status_code, 200)
        request = self.factory.get(reverse('get_user_info'))
        force_authenticate(request, self.test_user1)
        response = views.get_user_info(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('09130001122', response.data['phone'])

    def test_create_team(self):
        request = self.factory.post(reverse('create_team'), data={'name': 'TableFlipperZ'})
        force_authenticate(request, self.test_user1)
        response = views.create_team(request)
        self.assertEqual(response.status_code, 201)
        request = self.factory.get(reverse('get_team_info'))
        force_authenticate(request, self.test_user1)
        response = views.get_team_info(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'TableFlipperZ')
        self.assertIn(self.test_user1.email, response.data['members'])
        request = self.factory.post(reverse('send_team_invitation'), data={'email': 'pkazemi76@yahoo.com'})
        force_authenticate(request, self.test_user1)
        response = views.send_team_invitation(request)
        self.assertEqual(response.status_code, 201)
        # todo: Complete tests
