from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
  path('', views.index, name = 'index'),
  path('update_profile/<username>',views.update_profile,name='update_profile'),
  path('create_profile/', views.create_profile, name='create_profile'),
  
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)