from tortoise import fields, models


class UserModel(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)