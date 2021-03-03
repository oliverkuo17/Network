from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p"),
            "likes_number": self.likes.count(),
            "likes":[user.username for user in self.likes.all()],
        }

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")