from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 用户昵称
    nikename = models.CharField(max_length=20)

    def __str__(self):
        return 'user {}'.format(self.user.username)