from functools import partial
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.test import TestCase
# Add these imports at the top
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
import json

""" Test login"""


class TestLoginCase(TestCase):

    # Define the test client and other test variables.
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(email='testuser@gmail.com', password='12345')

    # Login with valid user and password
    def test_login_with_right_user_and_password_200_ok(self):
        login = self.client.post(
            reverse('login'),
            data={
                'email': 'testuser@gmail.com',
                'password': '12345'
            }
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)

    # Login with valid user and invalid password
    def test_login_with_right_user_and_wrong_password_401_UNAUTHORIZED(self):
        login = self.client.post(
            reverse('login'),
            data={
                'email': 'testuser@gmail.com',
                'password': '00000'
            }
        )
        self.assertEqual(login.status_code, status.HTTP_401_UNAUTHORIZED)

    # Login with username and without password
    def test_login_with_username_and_without_password_400_BAD_REQUEST(self):
        login = self.client.post(
            reverse('login'),
            data={
                'email': 'testuser@gmail.com',
                'password': ''
            }
        )
        self.assertEqual(login.status_code, status.HTTP_400_BAD_REQUEST)

    # Login without username and password
    def test_login_without_username_and_password_400_BAD_REQUEST(self):
        login = self.client.post(
            reverse('login'),
            data={
                'email': '',
                'password': ''
            }
        )
        self.assertEqual(login.status_code, status.HTTP_400_BAD_REQUEST)


""" Test refresh token"""


class TestRefreshTokenCase(TestCase):
    # Define the test client and other test variables.
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            email='testuser@gmail.com',
            password='12345'
        )
        # login
        login = self.login = self.client.post(
            reverse('login'),
            data={
                'email': 'testuser@gmail.com',
                'password': '12345'
            }
        )
        self.refresh = login.json()['refresh']
        self.access_token = login.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.headers = {"Content-Type": "application/json", 'Authorization': 'Bearer ' + self.access_token}

    # test valid refresh token
    def test_good_refresh_token_200_ok(self):
        refresh_token = self.client.post(
            reverse('token_refresh'),
            data={
                'refresh': self.refresh
            }
        )
        self.assertEqual(refresh_token.status_code, status.HTTP_200_OK)

    # request without refresh token
    def test_without_refresh_token_400_BAD_REQUEST(self):
        refresh_token = self.client.post(
            reverse('token_refresh')
        )
        self.assertEqual(refresh_token.status_code, status.HTTP_400_BAD_REQUEST)

    # test invalid refresh token
    def test_wrong_refresh_token_401_UNAUTHORIZED(self):
        refresh_token = self.client.post(
            reverse('token_refresh'),
            data={
                'refresh': "asfsdffdgadgdagd"
            }
        )
        self.assertEqual(refresh_token.status_code, status.HTTP_401_UNAUTHORIZED)

    # refresh token request after logout
    def test_refresh_token_after_logout_401_UNAUTHORIZED(self):
        logout = self.client.post(
            reverse('logout'),
            headers=self.headers,
            data={'refresh_token': self.refresh}
        )
        refresh_token = self.client.post(
            reverse('token_refresh'),
            data={
                'refresh': self.refresh
            }
        )
        self.assertEqual(refresh_token.status_code, status.HTTP_401_UNAUTHORIZED)


""" Test Change password"""


class TestChangePasswordCase(TestCase):
    # Define the test client and other test variables.
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            email='testuser@gmail.com',
            password='12345'
        )
        # login

        login = self.login = self.client.post(
            reverse('login'),
            data={
                'email': 'testuser@gmail.com',
                'password': '12345'
            }
        )
        self.refresh = login.json()['refresh']
        self.access_token = login.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.headers = {"Content-Type": "application/json", 'Authorization': 'Bearer ' + self.access_token}

    # test valid old password and valid new password
    def test_change_password_with_all_data_200_ok(self):
        change_password = self.client.patch(
            reverse('change_password'),
            headers=self.headers,
            data={
                'old_password': '12345',
                'new_password': '00000',
            }
        )
        self.assertEqual(change_password.status_code, status.HTTP_200_OK)

    # test with wrong old password
    def test_change_password_with_wrong_old_password_400_bad_request(self):
        change_password = self.client.patch(
            reverse('change_password'),
            headers=self.headers,
            data={
                'old_password': '123',
                'new_password': '00000',
            }
        )
        self.assertEqual(change_password.status_code, status.HTTP_400_BAD_REQUEST)

    # test without new password
    def test_change_password_without_new_password_400_bad_request(self):
        change_password = self.client.patch(
            reverse('change_password'),
            headers=self.headers,
            data={
                'old_password': '12345',
                'new_password': '',
            }
        )
        self.assertEqual(change_password.status_code, status.HTTP_400_BAD_REQUEST)

    # test without passwords
    def test_change_password_without_passwords_400_bad_request(self):
        change_password = self.client.patch(
            reverse('change_password'),
            headers=self.headers,
            data={
                'old_password': '',
                'new_password': '',
            }
        )
        self.assertEqual(change_password.status_code, status.HTTP_400_BAD_REQUEST)

    # test unauthenticated user
    def test_change_password_unauthenticated_user_401_unauthorized(self):
        new_client = APIClient()
        change_password = new_client.patch(
            reverse('change_password'),
            data={
                'old_password': '12345',
                'new_password': '00000',
            }
        )
        self.assertEqual(change_password.status_code, status.HTTP_401_UNAUTHORIZED)


""" Test register"""


class TestRegisterCase(TestCase):
    # Define the test client and other test variables.
    def setUp(self):
        self.client = APIClient()

    # request with all data
    def test_register_with_all_data_200_created(self):
        register = self.client.post(
            reverse('register'),
            data={
                'name': 'ahmed',
                'email': 'ahmed@gmail.com',
                'password': 'pass12345',
                'password2': 'pass12345',
                'country': 'Egypt',
                'the_outcome_of_forensic_science': 'good',
            }
        )
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)

    # request with mandatory data without first name and last name
    def test_register_with_mandatory_data_without_first_name_and_last_name_201_created(self):
        register = self.client.post(
            reverse('register'),
            data={
                'name': 'ahmed',
                'email': 'ahmed@gmail.com',
                'password': 'pass12345',
                'password2': 'pass12345',
                'country': 'Egypt',
                'the_outcome_of_forensic_science': 'good',
            }
        )
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)

    # request with small password
    def test_register_with_small_password_bad_request(self):
        register = self.client.post(
            reverse('register'),
            data={
                'name': 'ahmed',
                'email': 'ahmed@gmail.com',
                'password': 'pass',
                'password2': 'pass',
                'first_name': 'ahmed',
                'last_name': 'mohamed',
            }
        )
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    # request with small password not equal password2
    def test_register_with_password_not_equal_password2_400_bad_request(self):
        register = self.client.post(
            reverse('register'),
            data={
                'name': 'ahmed',
                'email': 'ahmed@gmail.com',
                'password': 'pass123456',
                'password2': 'pass11111',
                'first_name': 'ahmed',
                'last_name': 'mohamed',
            }
        )
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    # request with old username
    def test_register_with_old_account_400_bad_request(self):
        old_user = User.objects.create_superuser(
            name='ahmed',
            email='testuser@gmail.com',
            password='12345',
            country='Egypt',
            the_outcome_of_forensic_science='good',
        )
        register = self.client.post(
            reverse('register'),
            data={
                'name': 'ahmed',
                'email': 'ahmed@gmail.com',
                'password': 'pass123456',
                'password2': 'pass123456',
                'first_name': 'ahmed',
                'last_name': 'mohamed',
            }
        )
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    # request with old email
    def test_register_with_old_email_400_bad_request(self):
        old_user = User.objects.create_user(
            name='newuser',
            email='ahmed@gmail.com',
            password='12345'
        )
        register = self.client.post(
            reverse('register'),
            data={
                'name': 'ahmed',
                'email': 'ahmed@gmail.com',
                'password': 'pass123456',
                'password2': 'pass123456',

            }
        )
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    # request without email
    def test_register_without_email_400_bad_request(self):
        register = self.client.post(
            reverse('register'),
            data={
                'name': 'ahmed',
                'password': 'pass123456',
                'password2': 'pass123456',
            }
        )
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    # request without password
    def test_register_without_password_400_bad_request(self):
        register = self.client.post(
            reverse('register'),
            data={
                'name': 'ahmed',
                'email': 'ahmed@gmail.com',
                'password2': 'pass123456',
                'first_name': 'ahmed',
                'last_name': 'mohamed',
            }
        )
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    # request without password2
    def test_register_without_password2_400_bad_request(self):
        register = self.client.post(
            reverse('register'),
            data={
                'name': 'ahmed',
                'email': 'ahmed@gmail.com',
                'password': 'pass123456',
            }
        )
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    # request without all mandatory data
    def test_register_without_mandatory_data_400_bad_request(self):
        register = self.client.post(
            reverse('register'),
            data={
                'name': 'ahmed',
            }
        )
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)


""" Test logout """
import mock
from datetime import timedelta, datetime, timezone


class TestLogoutCase(TestCase):
    # Define the test client and other test variables.
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            name='testuser',
            email='testuser@gmail.com',
            password='12345'
        )
        # login

        login = self.login = self.client.post(
            reverse('login'),
            data={
                'email': 'testuser@gmail.com',
                'password': '12345'
            }
        )
        self.refresh = login.json()['refresh']
        self.access_token = login.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.headers = {"Content-Type": "application/json", 'Authorization': 'Bearer ' + self.access_token}

    # request with logged user
    def test_logout_with_good_refresh_token_200_ok(self):
        logout = self.client.post(
            reverse('logout'),
            headers=self.headers,
            data={
                'refresh_token': self.refresh,
                'new_password': '00000',
            }
        )
        self.assertEqual(logout.status_code, status.HTTP_200_OK)

    # request without logged user
    def test_logout_without_login_401_unauthorized(self):
        new_client = APIClient()
        logout = new_client.post(
            reverse('logout'),
            data={
                'refresh_token': self.refresh,
            }
        )
        self.assertEqual(logout.status_code, status.HTTP_401_UNAUTHORIZED)

    # request with bad refresh token
    def test_logout_with_bad_refresh_token_400_bad_request(self):
        logout = self.client.post(
            reverse('logout'),
            data={
                'refresh_token': 'jnknkklmlnknnjbn',
            }
        )
        self.assertEqual(logout.status_code, status.HTTP_400_BAD_REQUEST)

    # request without refresh token
    def test_logout_without_refresh_token_400_bad_request(self):
        logout = self.client.post(
            reverse('logout'))
        self.assertEqual(logout.status_code, status.HTTP_400_BAD_REQUEST)

    # test access token still valid after logout
    def test_access_token_still_valid_after_logout(self):
        logout = self.client.post(
            reverse('logout'),
            data={
                'refresh_token': self.refresh,
            }
        )
        # test function named hello
        hello = self.client.post(
            reverse('hello'),
            headers=self.headers,
        )
        self.assertEqual(hello.status_code, status.HTTP_200_OK)

    # test access token invalid in hour after logout
    def test_access_token_invalid_in_hour_after_logout(self):
        logout = self.client.post(
            reverse('logout'),
            data={
                'refresh_token': self.refresh,
            }
        )
        # test function named hello

        m = mock.Mock()
        m.return_value = datetime.now(timezone.utc) + timedelta(minutes=60)
        with mock.patch('rest_framework_simplejwt.tokens.aware_utcnow', m):
            hello = self.client.post(
                reverse('hello'),
                headers=self.headers,
            )
        self.assertEqual(hello.status_code, status.HTTP_401_UNAUTHORIZED)


""" Test reset password """


class TestResetPasswordCase(TestCase):
    # Define the test client and other test variables.
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            name='testuser',
            email='testuser@gmail.com',
            password='12345'
        )

    # test request with valid email
    def test_reset_password_with_valid_email_200_ok(self):
        reset_password = self.client.post(
            '/accounts/reset-password/',
            data={'email': 'testuser@gmail.com'}
        )
        self.assertEqual(reset_password.status_code, status.HTTP_200_OK)

    # test request with invalid email
    def test_reset_password_with_invalid_email_400_bad_request(self):
        reset_password = self.client.post(
            '/accounts/reset-password/',
            data={'email': 'testnewuser@gmail.com'}
        )
        self.assertEqual(reset_password.status_code, status.HTTP_400_BAD_REQUEST)

    # test request without email
    def test_reset_password_without_email_400_bad_request(self):
        reset_password = self.client.post(
            '/accounts/reset-password/',
        )
        self.assertEqual(reset_password.status_code, status.HTTP_400_BAD_REQUEST)
