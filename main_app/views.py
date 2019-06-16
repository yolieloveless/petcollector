from django.shortcuts import render
from django.http import HttpResponse
from .models import Pet


# Create your views here.
def home(request):
    return HttpResponse('<h1>Welcome to Pet Collector</h1>')

def about(request):
    return render(request, 'about.html')

def pets_index(request):
    pets = Pet.objects.all()
    return render(request, 'pets/index.html', { 'pets': pets })

def pets_detail(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    return render(request, 'pets/detail.html', { 'pet' : pet })

    