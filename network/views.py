import json
from django.contrib.admin.utils import flatten
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follower

def index(request):
    if request.method == "POST":
        content = request.POST["content"]
        if len(content) > 0:
            Post.objects.create(content=content, user=request.user)
        return HttpResponseRedirect(reverse("index"))
    all_posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(all_posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
            "page_obj": page_obj,
            "posts": all_posts,
        })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def post(request, post_id):
    post = Post.objects.get(pk=post_id)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post likes
    elif request.method == "PUT":
        data = json.loads(request.body)
        toggle_like = data.get("toggle_like", "")
        if toggle_like:
            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
        post.save()
        return JsonResponse({"message": "Post edited successfully", "likes_num": post.likes.count()}, status=201)


def profile(request, user_id):
    user_profile = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(user=user_id).order_by("-timestamp")
    paginator = Paginator(all_posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    profile_follower = Follower.objects.filter(user=user_profile)
    profile_follower_id = flatten(profile_follower.values_list('follower'))
    if request.method == "POST":
        if 'follow' in request.POST:
            Follower.objects.create(user=user_profile, follower=request.user)
        elif 'unfollow' in request.POST:
            Follower.objects.get(user=user_profile, follower=request.user).delete()
        return HttpResponseRedirect(reverse("profile", args=(user_id,)))
    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        "page_obj": page_obj,
        "profile_follower_id": profile_follower_id,
    })
