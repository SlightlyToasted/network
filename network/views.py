import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Post
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, "network/index.html")



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

#create new post
@csrf_exempt
def create(request):
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get content
    data = json.loads(request.body)
    content = data.get("content", "")

    new_post = Post(user=request.user, content=content)
    new_post.save()

    return JsonResponse({"message": "Post submitted successfully."}, status=201)

# get all posts in reverse chronological order
def posts(request):
    #Get all posts
    posts = Post.objects.all()

    #get most recent posts first
    posts = posts.order_by("-timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


def user(request, username):
    #find user by username
    user_data = User.objects.filter(username=username)[0]
    posts = Post.objects.filter(user=user_data)
    posts = posts.order_by("-timestamp").all()

    #check if user is self
    if request.user.id == user_data.id:
        #if same user
        not_user = False
        is_following = None
    else:
        not_user = True
        #check if user is following 
        is_following = request.user.following.filter(id=user_data.id).exists()

    return render(request, 'network/user.html', {
        "user": user_data,
        "username": user_data.username,
        "followers": user_data.followers.count(),
        "following": user_data.following.count(),
        "posts": posts,
        "not_user": not_user,
        "is_following": is_following,

    })

def follow(request, user_id):
     # Finding watchers based on the id
    user = User.objects.get(id=user_id)
    request.user.following.add(user)
    return redirect('user', user.username)

def unfollow(request, user_id):
    # Finding watchers based on the id
    user = User.objects.get(id=user_id)
    request.user.following.remove(user)
    return redirect('user', user.username)