
from django.test import TestCase
from django.conf import settings
from django.db import connection, models

from .models import (
    BaseModel,
    ActiveStatusModel,
    SoftDeleteModel,
    AuditModel,
)

class SoftDeleteTestRecord(SoftDeleteModel):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "core"
class TimestampedSoftDeleteTestRecord(BaseModel, SoftDeleteModel):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "core"


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
class SoftDeleteBehaviorTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(SoftDeleteTestRecord)
            schema_editor.create_model(TimestampedSoftDeleteTestRecord)

    @classmethod
    def tearDownClass(cls):
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(SoftDeleteTestRecord)
            schema_editor.delete_model(TimestampedSoftDeleteTestRecord)

        super().tearDownClass()

    def test_soft_delete_marks_record_as_deleted(self):
        record = SoftDeleteTestRecord.objects.create(
            name="Test record"
        )

        record.soft_delete()
        record.refresh_from_db()

        self.assertTrue(record.is_deleted)
        self.assertIsNotNone(record.deleted_at)

    def test_restore_recovers_soft_deleted_record(self):
        record = SoftDeleteTestRecord.objects.create(
            name="Test record"
        )

        record.soft_delete()
        record.restore()
        record.refresh_from_db()

        self.assertFalse(record.is_deleted)
        self.assertIsNone(record.deleted_at)

    def test_soft_delete_updates_timestamp(self):
        record = TimestampedSoftDeleteTestRecord.objects.create(
            name="Timestamp test"
        )

        original_updated_at = record.updated_at

        record.soft_delete()
        record.refresh_from_db()

        self.assertTrue(record.updated_at >= original_updated_at)
        self.assertTrue(record.is_deleted)