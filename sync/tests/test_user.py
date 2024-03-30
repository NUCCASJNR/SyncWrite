import unittest
from sync.models.user import MainUser as User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'first_name': 'dan',
            'last_name': 'hunter'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_creation(self):
        """Test that a user is created successfully"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        # Ensure that the user's password is set correctly
        self.assertTrue(self.user.check_password('testpassword'))

    def test_user_string_representation(self):
        """Test that the string representation of the user is correct"""
        self.assertEqual(str(self.user), str(self.user.email))

    def test_user_unique_email(self):
        """Test that the email field is unique"""
        # Attempt to create another user with the same email
        with self.assertRaises(Exception) as context:
            User.objects.create_user(
                username='anotheruser',
                email='testuser@example.com',  # Attempt to reuse the email
                password='anotherpassword'
            )
        # Ensure that the expected database integrity error is raised
        self.assertIn('duplicate entry', str(context.exception).lower())

    def tearDown(self):
        # Clean up after each test
        self.user.delete()


if __name__ == '__main__':
    unittest.main()
