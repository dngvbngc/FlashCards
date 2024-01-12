
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("sets", views.sets, name="sets"),
    path("make-new-set", views.make_set, name="make-set"),
    path("add-cards-csv/<int:set_id>", views.add_cards_csv, name="add-cards-csv"),
    path("view-set/<int:set_id>", views.set, name="view-set")
]
