from django.contrib import admin
from .models import Pet, Feeding, Photo

# Register your models here.
admin.site.register(Pet)
admin.site.register(Feeding)
admin.site.register(Photo)