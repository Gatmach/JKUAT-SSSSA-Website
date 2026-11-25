from types import SimpleNamespace

from django.contrib import admin
from django.contrib.auth.models import Group
from django.test import TestCase

from .admin import CustomGroupAdmin, CustomUserAdmin
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
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="StrongPassword123!",
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_email_is_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password="StrongPassword123!",
        )

    def test_create_user_strips_email_whitespace(self):
        user = User.objects.create_user(
            email="  student@example.com  ",
            password="StrongPassword123!",
        )

        self.assertEqual(user.email, "student@example.com")

    def test_create_user_rejects_invalid_email(self):
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email="invalid-email",
                password="StrongPassword123!",
            )

    def test_create_superuser_must_be_active(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com",
                password="StrongPassword123!",
                is_active=False,
            )

class CustomUserAdminPermissionTests(TestCase):

    def setUp(self):
        self.user_admin = CustomUserAdmin(User, admin.site)

    def test_ordinary_admin_cannot_manage_users(self):
        request = SimpleNamespace(
            user=SimpleNamespace(is_superuser=False)
        )

        self.assertFalse(
            self.user_admin.has_module_permission(request)
        )
        self.assertFalse(
            self.user_admin.has_view_permission(request)
        )
        self.assertFalse(
            self.user_admin.has_add_permission(request)
        )
        self.assertFalse(
            self.user_admin.has_change_permission(request)
        )
        self.assertFalse(
            self.user_admin.has_delete_permission(request)
        )

    def test_super_admin_can_manage_users(self):
        request = SimpleNamespace(
            user=SimpleNamespace(is_superuser=True)
        )

        self.assertTrue(
            self.user_admin.has_module_permission(request)
        )
        self.assertTrue(
            self.user_admin.has_view_permission(request)
        )
        self.assertTrue(
            self.user_admin.has_add_permission(request)
        )
        self.assertTrue(
            self.user_admin.has_change_permission(request)
        )
        self.assertTrue(
            self.user_admin.has_delete_permission(request)
        )


class CustomGroupAdminPermissionTests(TestCase):

    def setUp(self):
        self.group_admin = CustomGroupAdmin(Group, admin.site)

    def test_ordinary_admin_cannot_manage_groups(self):
        request = SimpleNamespace(
            user=SimpleNamespace(is_superuser=False)
        )

        self.assertFalse(
            self.group_admin.has_module_permission(request)
        )
        self.assertFalse(
            self.group_admin.has_view_permission(request)
        )
        self.assertFalse(
            self.group_admin.has_add_permission(request)
        )
        self.assertFalse(
            self.group_admin.has_change_permission(request)
        )
        self.assertFalse(
            self.group_admin.has_delete_permission(request)
        )

    def test_super_admin_can_manage_groups(self):
        request = SimpleNamespace(
            user=SimpleNamespace(is_superuser=True)
        )

        self.assertTrue(
            self.group_admin.has_module_permission(request)
        )
        self.assertTrue(
            self.group_admin.has_view_permission(request)
        )
        self.assertTrue(
            self.group_admin.has_add_permission(request)
        )
        self.assertTrue(
            self.group_admin.has_change_permission(request)
        )
        self.assertTrue(
            self.group_admin.has_delete_permission(request)
        )