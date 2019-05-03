from django.contrib import admin

from .models import Movie, Person, Vote


admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Vote)