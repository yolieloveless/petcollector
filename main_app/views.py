from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pet, Toy
from .forms import FeedingForm
import uuid
import boto3
from .models import Pet, Toy, Photo

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'petcollector'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid credentials - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
  

class PetCreate(LoginRequiredMixin, CreateView):
    model = Pet
    fields = ['name', 'breed', 'description', 'age']

def form_valid(self, form):
  form.instance.user = self.request.user
  return super().for_valid(form)

class PetUpdate(LoginRequiredMixin, UpdateView):
    model = Pet
    fields = ['breed', 'description', 'age']

class PetDelete(LoginRequiredMixin, DeleteView):
    model = Pet
    success_url = '/pets/'


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def pets_index(request):
    pets = Pet.objects.filter(user=request.user)
    return render(request, 'pets/index.html', { 'pets': pets })

@login_required
def pets_detail(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    toys_pet_doesnt_have = Toy.objects.exclude(id__in = pet.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'pets/detail.html', {
      'pet' : pet, 'feeding_form' : feeding_form,
      'toys': toys_pet_doesnt_have
   })

@login_required
def add_feeding(request, pet_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.pet_id = pet_id
    new_feeding.save()
  return redirect('detail', pet_id=pet_id)

@login_required
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

@login_required
def assoc_toy(request, pet_id, toy_id):
  Pet.objects.get(id=pet_id).toys.add(toy_id)
  return redirect('detail', pet_id=pet_id)

@login_required
def unassoc_toy(request, pet_id, toy_id):
  Pet.objects.get(id=pet_id).toys.remove(toy_id)
  return redirect('detail', pet_id=pet_id)

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'