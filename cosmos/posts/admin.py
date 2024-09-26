from django.contrib import admin

from .models import Post
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "content", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_filter = ["user", "updated", "timestamp"]
    list_editable = ["title", "user", "content"]

    search_fields = ["title", "content"]

    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)