from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default="default.jpg",upload_to="profilr_pics")
    bio=models.TextField(default="hi!")
    followers=models.ManyToManyField("self",related_name='followers',blank=True)
    request=models.ManyToManyField("self",related_name='request',blank=True)

    def __str__(self):
        return self.user.username
    def number_of_followers(self):
        return self.followers.count()
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.image.path)
        if img.height>100 or img.width>100:
            output_size=(100,100)
            img.thumbnail(output_size)
            img.save(self.image.path)




class friend_request(models.Model):
    from_user=models.ForeignKey(User,related_name='from_user',on_delete=models.CASCADE)
    to_user=models.ForeignKey(User,related_name='to_user',on_delete=models.CASCADE)
    def __str__(self):
        return self.from_user.username