from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from main import models, views, validators


class APITests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        models.Settings(key='test_key', value='test_value').save()
        self.test_user1 = models.User.objects.create_user(
            email='pkazemi3@gmail.com',
            password='pkazemi1376safe',
            first_name='Parham',
            last_name='Kazemi',
            phone='09130001122',
            institute='University of Isfahan',
            english_full_name='Parham Kazemi'
        )
        self.test_user2 = models.User.objects.create_user(
            email='pkazemi76@yahoo.com',
            password='pkazemi1376',
            first_name='Test',
            last_name='User',
            english_full_name='Test User',
            phone='09139998877',
            institute='University of Isfahan',
        )

    def test_settings(self):
        request = self.factory.get(reverse('get_settings'))
        response = views.get_settings(request)
        self.assertIn('test_key', response.data)

    def test_signup(self):
        data = {
            "email": "pkazemi3@gmail.com",
            "password": "pass1234",
            "first_name": "Parham",
            "last_name": "Kazemi",
            "phone": "09131002030",
            "institute": "University of Isfahan",
            "english_full_name": "Parham Kazemi"
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
        data.update({'english_full_name': 'پرهام کاظمی'})
        request = self.factory.post(reverse('sign_up'), data)
        response = views.sign_up(request)
        self.assertEqual(response.status_code, 400, 'Non-English name allowed')
        data.update({'english_full_name': 'Parham Kazemi', 'password': 'securePass1234'})
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


class UtilTests(TestCase):

    def test_team_name_regex_valid(self):
        test_cases = ['TableFlipperZ', 'RandomTeam123', 'team_name']
        for name in test_cases:
            try:
                validators.team_name_validator(name)
            except ValidationError:
                self.fail('Validation failed')

    def test_team_name_regex_invalid(self):
        test_cases = ['نام تیم', 'نباید', 'فارسی', 'باشد123_', 'team-name', 'team@name', 'team:name']
        for name in test_cases:
            self.assertRaises(ValidationError, validators.team_name_validator, name)

    def test_english_name_regex_valid(self):
        test_cases = ['Parham Kazemi', 'Parham', 'Kazemi', 'parham kazemi']
        for name in test_cases:
            try:
                validators.english_string_validator(name)
            except ValidationError:
                self.fail('Validation failed')

    def test_english_name_regex_invalid(self):
        test_cases = ['پرهام کاظمی', 'Parham کاظمی', 'Parham_Kazemi', 'Parham123']
        for name in test_cases:
            self.assertRaises(ValidationError, validators.english_string_validator, name)
