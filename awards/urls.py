from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
  path('', views.index, name = 'index'),
  path('update_profile/<username>',views.update_profile,name='update_profile'),
  path('create_profile/', views.create_profile, name='create_profile'),
  path('new/site', views.new_site, name = 'new_site'),
  path('search/', views.search, name='search'),
  path('project/<project>', views.project, name='project'),

  path('api/profiles/', views.ProfileList.as_view()),
  path('api/projects/', views.ProjecsList.as_view()),
  re_path(r'api/profile/profile-id/(?P<pk>[0-9]+)/$', views.ProfileDescription.as_view()),
  re_path(r'api/project/project-id/(?P<pk>[0-9]+)/$', views.ProjectDescription.as_view()),
  

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)