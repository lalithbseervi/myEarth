from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.shortcuts import get_object_or_404

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

        for user in User.objects.all():
            UserProfile.calculate_engagement_score(get_object_or_404(UserProfile, user=user))
            UserProfile.update_tag(user)