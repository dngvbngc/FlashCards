from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Set, Card

import csv
import pandas as pd
import io

def index(request):
    return render(request, "flashcards/index.html")

def make_set(request):
    message = None
    if request.method == "POST":
        set_name = request.POST["set_name"]
        set_description = request.POST["set_description"]
        number_of_terms = int(request.POST["nTerms"])
        if set_name:
            # First, save the set
            new_set = Set(
                owner=request.user,
                name=set_name,
                description=set_description
            )
            new_set.save()

            # Then, save the terms (if any):
            if number_of_terms > 0:
                for i in range(number_of_terms):
                    card_term = request.POST["card_{i}_term".format(i=i)]
                    card_definition = request.POST["card_{i}_definition".format(i=i)]
                    if card_term and card_definition:
                        new_card = Card(set=new_set,
                            term=card_term,
                            definition=card_definition
                        )
                        new_card.save()

            # Redirect user to add-cards-csv route if they selected csv:
            if request.POST["method"] == "csv":
                return HttpResponseRedirect(reverse('add-cards-csv', args=(new_set.pk,)))
            
            # Redirect user to sets page
            return HttpResponseRedirect(reverse("sets"))
        else:
            message = "Please add a name for your new set."

    return render(request, "flashcards/make-set.html", 
                  {"message": message}
                  )

def add_cards_csv(request, set_id):
    set = Set.objects.filter(pk=set_id).first()
    message = None

    if request.method == "POST":
        file = request.FILES.get("file")
        if file:
            file_name = file.name
            # Handle CSV file
            if file_name.endswith('.csv'):
                file = file.read().decode('utf-8')
                csv_reader = csv.reader(file.splitlines(), delimiter=',')
                for row in csv_reader:
                    if len(row) != 2:
                        message = "2 columns needed for each row. Only {l} row(s) detected. Please re-format your file and try again".format(l=len(row))
                        return render(request, "flashcards/add-cards-csv.html", {
                            "set": set,
                            "message": message
                        })
                    term, definition = row[0], row[1]
                    if term and definition:
                        new_card = Card(
                            set=set,
                            term=term,
                            definition=definition
                        )
                        new_card.save()
                return HttpResponseRedirect(reverse("sets"))
            
            elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            # Handle Excel file
                if file_name.endswith('.xlsx'):
                    df = pd.read_excel(file, engine='openpyxl')
                else:
                    df = pd.read_excel(file, engine='xlrd')
                if 'Term' in df.columns and 'Definition' in df.columns:
                    for index, row in df.iterrows():
                        # The excel file must have two columns name Term and Definition
                        term, definition = row['Term'], row['Definition']
                        if term and definition:
                            new_card = Card(
                                set=set,
                                term=term,
                                definition=definition
                            )
                            new_card.save()
                    return HttpResponseRedirect(reverse("sets"))
                else:
                    message = "Excel file does not follow correct format."
            
            else:
                message = "Unsupported file format."
        
        else: 
            message = "No files detected."
        
        return render(request, "flashcards/add-cards-csv.html", {
            "set": set,
            "message": message
        })
    
    return render(request, "flashcards/add-cards-csv.html", {
        "set": set,
        "message": message
    })

def sets(request):
    if request.user.is_authenticated:
        sets = request.user.sets.all()
        return render(request, "flashcards/sets.html", {
            "sets": sets
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
