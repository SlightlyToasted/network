from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', related_name="following", null=True)
    following = models.ManyToManyField('self', related_name="followers",null=True)

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    likes_users = models.ManyToManyField("User", related_name="likes", null=True)
    
    def __str__(self):
        return f"Post {self.id} from {self.user} at {self.timestamp}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes_user.count()
        }
