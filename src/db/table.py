import uuid

from tortoise import fields, models


class UserDBModel(models.Model):
    user_id = fields.UUIDField(default=uuid.uuid4, unique=True)
    name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=50)

    is_active = fields.BooleanField(default=True)
    role = fields.CharField(max_length=12, default="user")


class SessionDBModel(models.Model):
    user_id = fields.CharField(max_length=50)
    session_id = fields.CharField(max_length=50, unique=True)
