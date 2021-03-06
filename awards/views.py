from django.shortcuts import redirect, render
from django.http  import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UpdateProfile, CreateProfileForm, NewSiteForm, RatingsForm
from django.contrib.auth.decorators import login_required
from .models import Profile, User, Projects, Rating
import datetime as dt
from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer, ProjectsSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly
import random

# Create your views here.

def index(request):
  date=dt.date.today()
  username = request.user.username
  profile = Profile.get_user(username)
  projects = Projects.objects.all().order_by('-pub_date')
  random_project = ''
  if request.method == "POST":
    form = NewSiteForm(request.POST)
    if form.is_valid():
      project = form.save(commit=False)
      project.user = request.user
      project.save()
  else:
    form = NewSiteForm()

  try:
    projects = Projects.objects.all()
    projects = projects[::-1]
    a_project = random.randint(0, len(projects)-1)
    random_project = projects[a_project]
  except:
    projects = None   
  return render(request, 'index.html',{"date":date, "projects":projects, "profile": profile, 'form': form,'random_project': random_project})

@login_required
def new_site(request):
  current_user = request.user
  if request.method == 'POST':
    form = NewSiteForm(request.POST, request.FILES)
    if form.is_valid():
      site = form.save(commit=False)
      site.user = current_user
      site.save()
    return redirect('index')
  else:
    form = NewSiteForm()
  return render(request, 'submit_site.html', {"form":form})

@login_required  
def search(request):
    username = request.user.username
    profile = Profile.get_user(username)

    if 'search' in request.GET and request.GET["search"]:
        name = request.GET.get("search")
        searched_projects = Projects.search_project(name)
        print(searched_projects)
        message = f"{name}"

        return render(request, 'search_project.html',{"message":message,"projects": searched_projects, "username":username, "profile":profile})

    else:
        message = "You haven't searched for any term"
        
        return render(request, 'search_project.html',{"message":message})

 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created you are now able to login {username}')
            return redirect('login')
    else:
       form = UserRegisterForm()
    return render(request, 'users/register.html',{"form":form})   

# @login_required
# def profile(request):
#   if request.method == 'POST':
#     u_form = UserUpdateForm(request.POST, instance=request.user)
#     p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#     if u_form.is_valid() and p_form.is_valid():
#       u_form.save()
#       p_form.save()
#       messages.success(request, f'Your account has been updated')
#       return redirect('profile')
#   else:
#     u_form = UserUpdateForm(instance=request.user)
#     p_form = ProfileUpdateForm(instance=request.user.profile)

  
#   context ={
#     'u_form': u_form,
#     'p_form': p_form
#   }
#   return render(request, 'users/profile.html', context)
@login_required
def profile(request, username):
    '''
    Method to display a specific user profile
    '''
    profile = Profile.get_user(username)
    projects = Projects.user_projects(username)
    
    return render(request, 'users/profile.html', {"profile": profile, "projects":projects })

@login_required
def create_profile(request):
  current_user=request.user
  if request.method == 'POST':
    form = CreateProfileForm(request.POST,request.FILES)
    if form.is_valid():
      profile = form.save(commit=False)
      profile.user = current_user
      profile.save()
    return HttpResponseRedirect('/')
  else:
    form = CreateProfileForm()
  return render(request,'user/create_profile.html',{"form":form})



@login_required
def update_profile(request,username):
  user=User.objects.get(username=username)
  current_user = request.user
  
  if request.method =='POST':
    form = UpdateProfile(request.POST,request.FILES, instance=current_user.profile)
    
    if form.is_valid():
      form.save()
      return redirect('profile', user.username)
  
  else:
    form = UpdateProfile(instance=current_user.profile)
  
  return render(request,"users/update_profile.html", {"form":form})

@login_required
def project(request, project):
  project = Projects.objects.get(name=project)
  ratings = Rating.objects.filter(user=request.user, project=project).first()
  rating_status = None
  if ratings is None:
    rating_status = False
  else:
    rating_status = True
  if request.method == 'POST':
    form = RatingsForm(request.POST)
    if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project
            rate.save()
            project_ratings = Rating.objects.filter(project=project)

            design_ratings = [d.design for d in project_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in project_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in project_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
    return HttpResponseRedirect(request.path_info)
  else:
        form = RatingsForm()
  params = {
        'project': project,
        'rating_form': form,
        'rating_status': rating_status

    }
  return render(request, 'project.html', params)

class ProfileList(APIView):
  permission_classes = (IsAdminOrReadOnly,)
  def get(self, request, format=None):
    profiles = Profile.objects.all()
    serializers = ProfileSerializer(profiles, many=True)
    return Response(serializers.data)

  def post(self, request, format=None):
    serializers = ProfileSerializer(data=request.data)
    if serializers.is_valid():
      serializers.save()
      return Response(serializers.data, status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

class ProfileDescription(APIView):
  permission_classes = (IsAdminOrReadOnly,)
  def get_profile(self, pk):
    try:
      return Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
      return Http404

  def get(self, request, pk, format=None):
    profile = self.get_profile(pk)
    serializers = ProfileSerializer(profile)
    return Response(serializers.data)

   
class ProjecsList(APIView):
  permission_classes = (IsAdminOrReadOnly,)
  def get(self, request, format=None):
    projects = Projects.objects.all()
    serializers = ProjectsSerializer(projects, many=True)
    return Response(serializers.data)

  def post(self, request, format=None):
    serializers = ProjectsSerializer(data=request.data)
    if serializers.is_valid():
      serializers.save()
      return Response(serializers.data, status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDescription(APIView):
  permission_classes = (IsAdminOrReadOnly,)
  def get_project(self, pk):
    try:
      return Projects.objects.get(pk=pk)
    except Projects.DoesNotExist:
      return Http404

  def get(self, request, pk, format=None):
    project = self.get_project(pk)
    serializers = ProjectsSerializer(project)
    return Response(serializers.data)


    


