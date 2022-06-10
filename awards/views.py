from django.shortcuts import redirect, render
from django.http  import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UpdateProfile, CreateProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile, User

# Create your views here.

def index(request):
 

  return render(request, 'index.html', )
 
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
   
    
    return render(request, 'users/profile.html', {"profile": profile })

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
