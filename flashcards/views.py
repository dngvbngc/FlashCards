import json
import random

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Set, Card, Add

import csv
import pandas as pd
import io

def index(request):
    new_sets = Set.objects.all().order_by('-timestamp')[:5]
    paginator = Paginator(new_sets, 1)  # Show 1 set per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "flashcards/index.html", {
        "page_obj": page_obj
    })

def create(request):
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
            
            # Redirect user to collection page
            return HttpResponseRedirect(reverse("collection"))
        else:
            message = "Please add a name for your new set."

    return render(request, "flashcards/create.html", 
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
                return HttpResponseRedirect(reverse("collection"))
            
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
                    return HttpResponseRedirect(reverse("collection"))
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

def collection(request):
    if request.user.is_authenticated:
        user = request.user
        sets = user.sets.all()
        added = user.added.all()
        return render(request, "flashcards/collection.html", {
            "sets": sets,
            "added": added
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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not username or not password:
            return render(request, "flashcards/register.html", {
                "message": "Please input a username and password."
            })
        
        # Ensure password matches confirmation
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

def set(request, set_id):
    user = None
    message = None
    if request.user.is_authenticated:
        user = request.user
    else:
        message = "Log in to add this set to your collection, or edit and delete if you are the owner."

    try: 
        set = Set.objects.get(pk=set_id)

        # For one card view
        cards = set.cards.all()
        paginator = Paginator(cards, 1) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        user_is_not_owner = set.owner != user
        user_has_not_added = len(Add.objects.filter(user=user, set=set)) == 0
    except Set.DoesNotExist:
        return HttpResponseRedirect(reverse('error', args=(404,)))
    
    if request.method == "POST":
        action = request.POST["action"]
        if action == "add":
            if len(Add.objects.filter(user=user, set=set)) == 0:
                new_add = Add(user=request.user,set=set)
                new_add.save()
                return HttpResponseRedirect(reverse('view-set', args=(set.pk,)))
            else:
                message = "Set already added to your collection."
        elif action == "unadd":
            if len(Add.objects.filter(user=user, set=set)) == 1:
                Add.objects.filter(user=request.user, set=set).delete()
                return HttpResponseRedirect(reverse('view-set', args=(set.pk,)))
            else:
                message = "Set has not been added to your collection."
        elif action == "delete":
            Set.objects.filter(owner=user, pk=set_id).delete()
            return HttpResponseRedirect(reverse("collection"))
        elif action == "edit":
            if request.POST["set_name"]:
                set.name = request.POST["set_name"]
                set.description = request.POST["set_description"]
                set.save()
                current_cards_count = set.cards.all().count()
                current_cards = list(set.cards.all())
                nTerms = int(request.POST["nTerms"])
                for i in range(nTerms):
                    if i < current_cards_count:
                        current_card = current_cards[i]
                        card_term = request.POST["old_card_{pk}_term".format(pk=current_card.pk)]
                        card_definition = request.POST["old_card_{pk}_definition".format(pk=current_card.pk)]
                        if card_term and card_definition:
                            current_card.term = card_term
                            current_card.definition = card_definition
                            current_card.save()
                        else:
                            current_card.delete()
                    else:
                        card_term = request.POST["card_{i}_term".format(i=i)]
                        card_definition = request.POST["card_{i}_definition".format(i=i)]
                        if card_term and card_definition:
                            new_card = Card(set=set, term=card_term, definition=card_definition)
                            new_card.save()
                return HttpResponseRedirect(reverse('view-set', args=(set.pk,)))
            else:
                message = "Edit invalid. Please input a name and description for your set."
        return render(request, "flashcards/set.html", {
            "set": set,
            "user_is_not_owner": user_is_not_owner,
            "user_has_not_added": user_has_not_added,
            "message": message,
            "page_obj": page_obj
        })
    
    return render(request, "flashcards/set.html", {
            "set": set,
            "user_is_not_owner": user_is_not_owner,
            "user_has_not_added": user_has_not_added,
            "message": message,
            "page_obj": page_obj
        })
        
def study(request, set_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('error', args=(400,)))
    
    try:
        set = Set.objects.get(pk=set_id)
        cards = set.cards.all()
        # Shuffle the cards
        shuffled = [None] * len(cards)
        index = -1
        
        for card in cards:
            while index == -1 or shuffled[index] is not None:
                index = random.randint(0, len(cards) - 1)
            shuffled[index] = card

        paginator = Paginator(shuffled, 1)  
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    except Set.DoesNotExist:
        return HttpResponseRedirect(reverse('error', args=(404,)))
    
    return render(request, "flashcards/study.html", {
        "set": set,
        "page_obj": page_obj
    })

def error(request, error_code):
    message = None
    if error_code == 404:
        message = "Invalid set ID."
    if error_code == 400:
        message = "This action require log in."
    return render(request, "flashcards/error.html", {
        "message": message
    })