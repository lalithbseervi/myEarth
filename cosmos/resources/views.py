from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from .models import Submission

# Create your views here.
def index(request):
    return render(request, 'resources/index.html')

@csrf_protect
@login_required
def upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        Submission.objects.create(user = request.user, file = file, title = title, description = description).save()
    else:
        return render(request, 'resources/submission form.html')
    return render(request, 'resources/success.html')

def submit(request):
    return render(request, 'resources/submission form.html')

def resources(request):
    submissions = Submission.objects.all().order_by('-uploaded_at')

    return render(request, 'resources/resources.html', {'submissions': submissions})

#project start date: aug 23rd, 2024