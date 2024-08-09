from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Friend(models.Model):
    user = models.ForeignKey(User,related_name="profile",on_delete=models.CASCADE,null=True)
    friends = models.ForeignKey(User,related_name="friends_profile",on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.username

class FriendsGroup(models.Model):
    group_name = models.CharField(max_length=100)
    friends = models.ManyToManyField(User,related_name="group")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_groups", default=1)

    def __str__(self):
        return self.group_name