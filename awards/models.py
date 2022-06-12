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
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
  user = models.ForeignKey(User, related_name='posted_by', on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def save_project(self):
    self.save()

  def delete_project(self):
    self.delete() 

  def voters_num(self):
    return self.voters.count()

  @classmethod
  def get_all_projects(cls):
    return cls.objects.all()

  @classmethod
  def get_projects(cls, id):
    return Projects.objects.get(id=id)  

  @classmethod
  def search_project(cls, name):
    return cls.objects.filter(name__icontains=name).all() 

  @classmethod
  def user_projects(cls, username):
    return cls.objects.filter(user__username__contains=username)

  class Meta:
    ordering=['-pub_date']             


class Rating(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating, blank=True)
    content = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rater')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='ratings', null=True)

    def save_rating(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(project_id=id).all()
        return ratings

    def __str__(self):
        return f'{self.project} Rating'
