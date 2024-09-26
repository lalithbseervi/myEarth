from django.contrib.auth import (
    authenticate,
    login,
    logout,
    )
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, UserRegistrationForm, EditUserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import UserProfile

def login_view(request):
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")

    return render(request, "form.html", {"form": form, "title": title})

def register_view(request):
    path = request.GET.get('next')
    title = 'Register'
    form = UserRegistrationForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = form.save()

        new_user = authenticate(username=username, password=password)
        if new_user is not None:
            login(request, new_user)

            if path:
                return redirect(path)
            return redirect('/')
    else:
        print("Form invalid")

    context = {
        "form": form,
        "title": title
    }

    return render(request, "form.html", context)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    username = user.username
    email = user.email

    context = {
        "post_count": user_profile.get_post_count,
        "comments_count": user_profile.get_comment_count,
        "resources_uploaded": user_profile.get_resources_uploaded_count,
        "posts": user_profile.get_recent_posts,
        "submissions": user_profile.get_submissions,
        "tag": user_profile.tag,
        "username": username,
        "email": email
    }

    return render(request, "accounts/profile.html", context)

@login_required
def edit_profile(request, username):
    title = 'Edit Profile'
    if request.user.username == username:
        if request.method == 'POST':
            form = EditUserProfile(request.POST)
            if form.is_valid():
                user = request.user
                user.username = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                user.save()
                return redirect('profile', username=user.username)
        else:
            form = EditUserProfile(initial = {
                'username': request.user.username,
                'email': request.user.email,
            })
    else:
        return redirect('edit_profile', username=request.user.username)

    context = {
        "form": form,
        "title": title
    }

    return render(request, "form.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")