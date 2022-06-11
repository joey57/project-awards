from tkinter import CASCADE
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

  def save_profile(self):
    self.save() 

  def delete_profile(self):
    self.delete()   
       
  @classmethod
  def update_profile(cls,id,profile_pic,name,bio):
        cls.objects.filter(id=id).update(profile_pic=profile_pic,name=name,bio=bio)   
        
  @classmethod
  def get_user(cls,username):
     profile = cls.objects.filter(user__username__icontains=username)
     return profile  

class Projects(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  project_image = CloudinaryField('project_pics/')
  url = models.URLField()
  pub_date = models.DateTimeField(auto_now_add=True)
  profile = models.ForeignKey(Profile, on_delete=CASCADE, null=True)
  user = models.ForeignKey(User, related_name='posted_by', on_delete=models.CASCADE)

  def __str__(self):
    return self.name