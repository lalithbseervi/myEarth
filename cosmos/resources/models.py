from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Submission(models.Model):
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    title = models.CharField(max_length=127)
    description = models.TextField()
    uploaded_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} submitted by {self.user.username}"