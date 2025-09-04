from tortoise import fields, models


class UserDBModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    last_name = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=50, unique=True)

    is_active = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)