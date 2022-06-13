from rest_framework import serializers
from .models import Profile, Projects, Rating

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('id', 'user', 'name', 'image', 'bio')

class ProjectsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Projects
    fields = ('id', 'name', 'description', 'project_image', 'pub_date', 'profile', 'user')
