from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Pet, Toy
from .forms import FeedingForm
import uuid
import boto3
from .models import Pet, Toy, Photo

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'petcollector'

class PetCreate(CreateView):
    model = Pet
    fields = '__all__'

class PetUpdate(UpdateView):
    model = Pet
    fields = ['breed', 'description', 'age']

class PetDelete(DeleteView):
    model = Pet
    success_url = '/pets/'


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def pets_index(request):
    pets = Pet.objects.all()
    return render(request, 'pets/index.html', { 'pets': pets })

def pets_detail(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    toys_pet_doesnt_have = Toy.objects.exclude(id__in = pet.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'pets/detail.html', {
      'pet' : pet, 'feeding_form' : feeding_form,
      'toys': toys_pet_doesnt_have
   })

def add_feeding(request, pet_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.pet_id = pet_id
    new_feeding.save()
  return redirect('detail', pet_id=pet_id)

def add_photo(request, pet_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, pet_id=pet_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', pet_id=pet_id)

def assoc_toy(request, pet_id, toy_id):
  Pet.objects.get(id=pet_id).toys.add(toy_id)
  return redirect('detail', pet_id=pet_id)

def unassoc_toy(request, pet_id, toy_id):
  Pet.objects.get(id=pet_id).toys.remove(toy_id)
  return redirect('detail', pet_id=pet_id)

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'