
import uuid

from django.db import models
from django.utils import timezone
from django.conf import settings


class BaseModel(models.Model):
    """
    Abstract base model providing common fields
    for application database models.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class ActiveStatusModel(models.Model):
    """
    Optional abstract model for records that can
    be activated or deactivated.
    """

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Optional abstract model supporting soft deletion
    and restoration without physically deleting records.
    """

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class AuditModel(models.Model):
    """
    Optional abstract model that tracks the users
    responsible for creating and updating a record.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        abstract = True

