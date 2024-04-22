from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_video = models.ForeignKey(Video, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    like_video = models.ForeignKey(Video, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Subscribe(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    subscribee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribee')
    subscribed_at = models.DateTimeField(auto_now_add=True)

class Detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.URLField(null=True)
    profile_cover = models.URLField(null=True)
    user_description = models.TextField()

class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    replied_on = models.ForeignKey(Comment, on_delete=models.CASCADE)
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)