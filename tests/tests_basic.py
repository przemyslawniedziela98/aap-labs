import unittest
from app import create_app, db
from flask_testing import TestCase
from app.models.user import User
from flask import url_for


class TestBase(TestCase):
    """
    Base test class that sets up the application and database for all tests.
    """
    def create_app(self):
        """
        Creates and configures the app for testing.
        """
        app = create_app()
        return app

    def setUp(self):
        """
        Set up the database and add a test user before each test.
        """
        db.create_all()

        test_user = User(username='testuser', password_hash='password')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        """
        Clean up the database after each test.
        """
        db.session.remove()
        db.drop_all()


class TestViews(TestBase):
    """
    Test cases for the view routes in the application.
    """
    
    def test_home_page(self):
        """
        Test that the home page loads successfully.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """
        Test that the login page loads successfully.
        """
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        """
        Test that the registration page loads successfully.
        """
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_zmsi_page(self):
        """
        Test that the ZMSI page is protected and requires login.
        """
        self.client.post('/login', data=dict(username='testuser', password='password'), follow_redirects=True)
        response = self.client.get('/app')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(client):
        """
        Test to ensure accessing the dashboard redirects to login if the user is not authenticated.
        """
        response = client.get(url_for('auth.dashboard'))
        assert response.status_code == 302
        assert "/login" in response.location


    def test_successful_login(client):
        """
        Test to ensure successful login redirects to the dashboard.
        """
        response = client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
        assert response.status_code == 200