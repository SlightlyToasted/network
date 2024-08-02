import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Post
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



def index(request):
    return redirect('all_posts', 1)

def all_posts(request, page_num):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all() 

    #create paginator object
    p = Paginator(posts, 10)
    page_obj = p.get_page(page_num)

    #deal with prev page
    prev_page = None
    has_prev_page = False
    if page_obj.has_previous():
        prev_page = page_obj.previous_page_number()
        has_prev_page = True

    #deal with next page
    next_page = None
    has_next_page = False
    if page_obj.has_next():
        next_page = page_obj.next_page_number()
        has_next_page = True

    return render(request, 'network/all.html', {
        "username":request.user,
        "posts": page_obj,
        "pages": p,
        "prev_page": prev_page,
        "has_prev_page": has_prev_page,
        "next_page": next_page,
        "has_next_page": has_next_page,
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


def user(request, username, page_num):
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
        is_following = request.user.followers.filter(id=user_data.id).exists()

    #Paginator stuff
    p = Paginator(posts, 10)
    page_obj = p.get_page(page_num)

    #deal with prev page
    prev_page = None
    has_prev_page = False
    if page_obj.has_previous():
        prev_page = page_obj.previous_page_number()
        has_prev_page = True

    #deal with next page
    next_page = None
    has_next_page = False
    if page_obj.has_next():
        next_page = page_obj.next_page_number()
        has_next_page = True


    return render(request, 'network/user.html', {
        "user_data": user_data,
        "username": user_data.username,
        "followers": user_data.followers.count(),
        "following": user_data.following.count(),
        "posts": page_obj,
        "not_user": not_user,
        "is_following": is_following,
        "pages": p,
        "has_prev_page": has_prev_page,
        "prev_page": prev_page,
        "has_next_page": has_next_page,
        "next_page": next_page,

    })

def follow(request, user_id):
     # Finding followers based on the id
    
    user_to_follow = User.objects.get(id=user_id)
    print(user_to_follow)
    print(user_to_follow.followers.filter(id=user_to_follow.id).exists())
    user_to_follow.followers.add(request.user)

    print(user_to_follow.followers.filter(id=user_to_follow.id).exists())
    return redirect('user', user_to_follow.username, 1)

def unfollow(request, user_id):
    # Finding watchers based on the id
    user_to_unfollow = User.objects.get(id=user_id)
    user_to_unfollow.followers.remove(request.user)
    return redirect('user', user_to_unfollow.username, 1)


def following(request, page_num):
    following = User.objects.filter(followers=request.user)
    following = Post.objects.filter(user__in=following)
    posts = following.order_by("-timestamp").all() 

    #create paginator object
    p = Paginator(posts, 10)
    page_obj = p.get_page(page_num)

    #deal with prev page
    prev_page = None
    has_prev_page = False
    if page_obj.has_previous():
        prev_page = page_obj.previous_page_number()
        has_prev_page = True

    #deal with next page
    next_page = None
    has_next_page = False
    if page_obj.has_next():
        next_page = page_obj.next_page_number()
        has_next_page = True

    return render(request, 'network/following.html', {
        "username":request.user,
        "posts": page_obj,
        "pages": p,
        "prev_page": prev_page,
        "has_prev_page": has_prev_page,
        "next_page": next_page,
        "has_next_page": has_next_page,
    })