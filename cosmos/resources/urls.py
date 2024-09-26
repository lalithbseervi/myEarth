from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submission-form'),
    path('upload/', views.upload, name='upload'),
    path('resources/', views.resources, name='resources')
]