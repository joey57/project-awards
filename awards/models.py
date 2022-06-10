from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime as dt

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = CloudinaryField('profile_pics/',default='default.jpg')
  bio = models.TextField(max_length=500, default='My Bio', blank=True)
  name = models.CharField(max_length=250, blank=True)

  def __str__(self):
    return f'{self.user.username} Profile'

        
  @classmethod
  def update_profile(cls,id,profile_pic,name,bio):
        cls.objects.filter(id=id).update(profile_pic=profile_pic,name=name,bio=bio)   
        
  @classmethod
  def get_user(cls,username):
     profile = cls.objects.filter(user__username__icontains=username)
     return profile  
