from django.contrib import admin
from main.models import *

# Register your models here.
admin.site.register(Article)
admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Note)
admin.site.register(Flashcard)