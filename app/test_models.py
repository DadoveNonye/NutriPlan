import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_set_password(self):
        user = User()
        password = "password123"
        user.set_password(password)
        self.assertIsNotNone(user.password_hash)
        self.assertNotEqual(user.password_hash, password)

    def test_check_password(self):
        user = User()
        password = "password123"
        user.set_password(password)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.check_password("wrongpassword"))

    def test_repr(self):
        user = User(username="testuser")
        self.assertEqual(repr(user), "<User testuser>")

if __name__ == '__main__':
    unittest.main()
