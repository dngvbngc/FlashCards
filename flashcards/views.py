from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Set, Card


def index(request):
    message = None
    if request.method == "POST":
        set_name = request.POST["set_name"]
        set_description = request.POST["set_description"]
        if set_name:
            new_set = Set(
                owner=request.user,
                name=set_name,
                description=set_description
            )
            new_set.save()
            return HttpResponseRedirect(reverse("sets"))
        else:
            message = "Please add a name for your new set."

    return render(request, "flashcards/index.html", 
                  {"message": message}
                  )

def sets(request):
    if request.user.is_authenticated:
        sets = request.user.sets.all()
        return render(request, "flashcards/sets.html", 
                  {"sets": sets}
                  )


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
            return render(request, "flashcards/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "flashcards/login.html")


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
            return render(request, "flashcards/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "flashcards/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flashcards/register.html")
