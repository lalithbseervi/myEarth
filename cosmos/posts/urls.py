from django.urls import re_path as url, path
from django.contrib import admin

from .views import ( post_list, post_create, post_detail, post_update, post_delete, decorum )

urlpatterns = [
    url(r'^$', post_list, name='list'),
	url(r'^create/$', post_create),
	path('rules/', decorum, name='rules'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    path('<slug:slug>/', post_detail, name='detail_view'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]
