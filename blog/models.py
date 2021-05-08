from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
# Create your models here.

class posts(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_like')
    date_posted=models.DateTimeField(default=timezone.now)
    image=models.ImageField(upload_to="post_pic",default="default.jpg")

    def __str__(self):
        return self.title
    def number_of_likes(self):
        return self.likes.count()
    def save(self):
        super().save()
        img=Image.open(self.image.path)
        if img.height>500 or img.width>500:
            output_size=(500,500)
            img.thumbnail(output_size)
            img.save(self.image.path)


class comments(models.Model):
    post=models.ForeignKey(posts,related_name="comments",on_delete=models.CASCADE)
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.post}comment"

class savedposts(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    posts=models.ManyToManyField(posts)

    def __str__(self):
        return f"{self.user}savedposts"