from django.contrib.auth.models import User
from django.urls import reverse
from django.db import connection
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Portfolio

class databaseConnectionTests(APITestCase):
    def test_database_connection(self):
        """
        Test to ensure that the database connection is working.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1") # Simple query to test connection
                row = cursor.fetchone()
                db_connected = row is not None #If row then connection is successful
        except Exception as e:
            db_connected = False # If any exception occurs, connection failed
        self.assertTrue(db_connected, "Database connection failed.")

class UsersAccountTests(APITestCase): # Test for user registration and login
    def setUp(self):
        # Test user data
        self.username = "testuser"
        self.email = "test@example.com"
        self.password = "StrongP@ssw0rd!"
        # Create user in test database
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )

    def test_user_registration(self):
        # Test user registration endpoint
        url = reverse('register')  
        data = { # Creates a new user
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewStrongP@ssw0rd!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("ALERT", response.data)
        self.assertEqual(response.data["ALERT"], "User registered successfully")
        print(response.status_code, response.data)

    def test_user_login(self):
        # Test user login endpoint
        url = reverse('token_obtain_pair')  
        data = { # Logs in the previously created user
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data) # Checks for access JWT token
        self.assertIn("refresh", response.data) # Checks for refresh JWT token
        print(response.status_code)

    def test_user_update(self):
        # Test user update endpoint
        url = reverse('user-update')  
        self.client.login(username=self.username, password=self.password) # Log in the test user
        data = { # New data for updating user
            "username": "updateduser",
            "email": "updateduser@example.com",
            "password": self.password,
            "new_password": "UpdatedStrongP@ssw0rd!"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("ALERT", response.data)
        self.assertEqual(response.data["ALERT"], "User updated successfully")
        print(response.status_code, response.data)
        
        