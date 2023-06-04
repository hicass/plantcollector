import boto3
import uuid
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from .models import Plant, GrowingMedia, Photo
from .forms import WateringForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def plants_index(request):
    plants = Plant.objects.filter(user=request.user)

    return render(request, 'plants/index.html', {
        'plants': plants
    })


@login_required
def plants_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    id_list = plant.growing_media.all().values_list('id')
    growing_media_plant_doest_use = GrowingMedia.objects.exclude(id__in=id_list)
    watering_form = WateringForm()

    return render(request, 'plants/detail.html', {
        'plant': plant,
        'watering_form': watering_form,
        'growing_media': growing_media_plant_doest_use
    })


class PlantCreate(LoginRequiredMixin, CreateView):
    model = Plant
    fields = ['name', 'family', 'care']

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    fields = ['family', 'care']



class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    success_url = '/plants'


@login_required
def add_watering(request, plant_id):
    form = WateringForm(request.POST)
    if form.is_valid():
        new_watering = form.save(commit=False)
        new_watering.plant_id = plant_id
        new_watering.save()

    return redirect('detail', plant_id=plant_id)


class GrowingMediaList(LoginRequiredMixin, ListView):
    model = GrowingMedia


class GrowingMediaDetail(LoginRequiredMixin, DetailView):
    model = GrowingMedia


class GrowingMediaCreate(LoginRequiredMixin, CreateView):
    model = GrowingMedia
    fields = '__all__'


class GrowingMediaUpdate(LoginRequiredMixin, UpdateView):
    model = GrowingMedia
    fields = '__all__'


class GrowingMediaDelete(LoginRequiredMixin, DeleteView):
    model = GrowingMedia
    success_url = '/growing_med'


@login_required
def assoc_growing_med(request, plant_id, growing_med_id):
    Plant.objects.get(id=plant_id).growing_media.add(growing_med_id)

    return redirect('detail', plant_id=plant_id)


@login_required
def unassoc_growing_med(request, plant_id, growing_med_id):
    Plant.objects.get(id=plant_id).growing_media.remove(growing_med_id)

    return redirect('detail', plant_id=plant_id)


@login_required
def add_photo(request, plant_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"

            Photo.objects.create(url=url, plant_id=plant_id)

        except Exception as e:
            print('An error occured uploading file to S3')
            print(e)

    return redirect('detail', plant_id=plant_id)


def signup(request):
    error_message = ''

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('index')

        else:
            error_message = 'Invalid sign up - try again.'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}

    return render(request, 'registration/signup.html', context)