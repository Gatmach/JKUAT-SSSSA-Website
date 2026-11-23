
from django.test import TestCase

from .models import BaseModel, ActiveStatusModel, SoftDeleteModel
from django.conf import settings

class CoreModelTests(TestCase):

    def test_base_model_is_abstract(self):
        self.assertTrue(BaseModel._meta.abstract)

    def test_active_status_model_is_abstract(self):
        self.assertTrue(ActiveStatusModel._meta.abstract)
        self.assertTrue(
            ActiveStatusModel._meta.get_field("is_active").default
        )

    def test_soft_delete_model_is_abstract(self):
        self.assertTrue(SoftDeleteModel._meta.abstract)

    def test_soft_delete_fields_exist(self):
        self.assertTrue(
            SoftDeleteModel._meta.get_field("is_deleted").default is False
        )

        self.assertTrue(
            SoftDeleteModel._meta.get_field("deleted_at").null
        )
    def test_audit_model_is_abstract_and_uses_custom_user(self):
        from .models import AuditModel

        self.assertTrue(AuditModel._meta.abstract)

        self.assertEqual(
            AuditModel._meta.get_field("created_by").remote_field.model,
            settings.AUTH_USER_MODEL,
        )

        self.assertEqual(
            AuditModel._meta.get_field("updated_by").remote_field.model,
            settings.AUTH_USER_MODEL,
        )
