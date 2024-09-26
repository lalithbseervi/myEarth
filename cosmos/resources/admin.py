from django.contrib import admin
from .models import Submission

# Register your models here.
class FileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'uploaded_at')
    list_filter = ('uploaded_at', 'user',)
    search_fields = ('file', 'user', 'title', 'description')
admin.site.register(Submission)