from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

from posts.models import Post
from comments.models import Comment
from resources.models import Submission

import statistics
# Create your models here.
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    engagement_score = models.FloatField(null=True, blank=True)
    tag = models.CharField(max_length=32, null=True, blank=True)

    def get_post_count(self):
        return Post.objects.filter(user=self.user).count()

    def get_comment_count(self):
        return Comment.objects.filter(user=self.user).count()

    def get_resources_uploaded_count(self):
        return Submission.objects.filter(user=self.user).count()

    def get_recent_posts(self):
        return Post.objects.filter(user=self.user).order_by('-timestamp')[:5]

    def get_submissions(self):
        return Submission.objects.filter(user=self.user)

    def calculate_engagement_score(self):
        resources_w = 3.0
        post_w = 2.5
        comment_w = 1.0
        base = 1.0

        self.engagement_score = (resources_w * self.get_resources_uploaded_count() +
                                 post_w * self.get_post_count() +
                                 comment_w * self.get_comment_count() +
                                 base)
        self.save()

    def update_tag(self):
        scores = list(UserProfile.objects.values_list('engagement_score', flat=True))
        scores = [score for score in scores if score is not None]

        print(scores)

        mean = statistics.mean(scores) if scores else 0
        std_dev = statistics.stdev(scores) if len(scores) > 1 else 0

        low_threshold = mean - std_dev
        high_threshold = mean + std_dev

        for profile in UserProfile.objects.all():
            if profile.engagement_score is not None:
                if profile.engagement_score < low_threshold or profile.engagement_score == low_threshold:
                    profile.tag = 'New contributor'
                elif profile.engagement_score >= mean and profile.engagement_score < high_threshold:
                    profile.tag = 'Active contributor'
                elif profile.engagement_score == high_threshold:
                    profile.tag = 'Senior contributor'
                elif profile.engagement_score > high_threshold:
                    profile.tag = 'Veteran'
                else:
                    profile.tag = 'New contributor'
            profile.save()