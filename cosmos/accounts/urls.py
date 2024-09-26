from .views import (login_view, register_view, logout_view, profile, edit_profile)
from django.urls import re_path as url, path

urlpatterns = [
    url(r'^register/', view=register_view, name='register'),
    url(r'^login/', view=login_view, name='login'),
    url(r'^logout/', view=logout_view, name='logout'),
    path('profile/<str:username>/', view=profile, name='profile'),
    path('profile/<str:username>/edit/', view=edit_profile, name='edit_profile')
]