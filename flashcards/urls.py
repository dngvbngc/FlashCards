
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("collection", views.collection, name="collection"),
    path("create", views.create, name="create"),
    path("add-cards-csv/<int:set_id>", views.add_cards_csv, name="add-cards-csv"),
    path("view-set/<int:set_id>", views.set, name="view-set"),
    path("study-set/<int:set_id>", views.study, name="study-set"),
    path("test-set/<int:set_id>", views.test, name="test-set"),
    path("error/<int:error_code>", views.error, name="error")
]
