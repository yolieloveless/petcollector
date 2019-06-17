from django.contrib import admin
from .models import Pet, Feeding

# Register your models here.
admin.site.register(Pet)
admin.site.register(Feeding)