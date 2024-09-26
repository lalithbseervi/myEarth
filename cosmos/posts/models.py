from __future__ import unicode_literals

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from django.contrib.auth.models import User
from markdownx.utils import markdownify
from comments.models import Comment

from .utils import get_read_time

# Create your models here.
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
    
def upload_location(instance, filename):
    PostModel = instance.__class__
    new_id = PostModel.objets.order_by("id").last().id + 1
    return "%s/%s" %(new_id, filename)

class Post(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    height_field = models.IntegerField(default=50)
    width_field = models.IntegerField(default=100)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=True)
    read_time = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) 

    objects = PostManager()

    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("detail_view", kwargs={"slug": self.slug})
    
    class Meta:
        ordering = [
            "-timestamp",
            "-updated"
        ]

    def get_markdown(self):
        content = self.content
        markdown_text = markdownify(content)
        return mark_safe(markdown_text)
    
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs
    
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
    
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time = get_read_time(html_string)
        instance.read_time = read_time

pre_save.connect(pre_save_post_receiver, sender=Post)