from django.contrib import admin
from flashcards.models import User, Set, Card, Add

# Register your models here.
admin.site.register(User)
admin.site.register(Set)
admin.site.register(Card)
admin.site.register(Add)
