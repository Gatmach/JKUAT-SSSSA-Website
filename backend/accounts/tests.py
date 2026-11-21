from django.test import TestCase

from .models import User


class UserManagerTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            email="student@example.com",
            password="StrongPassword123!",
        )

        self.assertEqual(user.email, "student@example.com")
        self.assertTrue(user.check_password("StrongPassword123!"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            password="StrongPassword123!",
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_email_is_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password="StrongPassword123!",
            )