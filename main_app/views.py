from django.shortcuts import render
from django.http import HttpResponse

class Pet:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

pets = [
    Pet('Marley', 'Chihuahua', 'Black and white with black spots.  Queen of Everything.', 1),
    Pet('Dahlia', 'Chihuahua-Dachsund Mix', 'Loves to cuddle and sleep all day.', 7), 
    Pet('Jumpy', 'Frog', 'Loves to play in water.', 1)
]

# Create your views here.
def home(request):
    return HttpResponse('<h1>Welcome to Pet Collector</h1>')

def about(request):
    return render(request, 'about.html')

def pets_index(request):
    return render(request, 'pets/index.html', { 'pets': pets })