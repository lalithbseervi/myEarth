from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404

User = get_user_model()

class Command(BaseCommand):
    help = 'Update UserProfile for all existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        for user in users:
            UserProfile.calculate_engagement_score(get_object_or_404(UserProfile, user=user))
            UserProfile.update_tag(self)
            
        self.stdout.write(self.style.SUCCESS('Successfully updated UserProfiles for all users'))