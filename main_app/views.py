import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Plant, GrowingMedia, Photo
from .forms import WateringForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def plants_index(request):
    plants = Plant.objects.all()

    return render(request, 'plants/index.html', {
        'plants': plants
    })


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


class PlantCreate(CreateView):
    model = Plant
    fields = ['name', 'family', 'care']

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class PlantUpdate(UpdateView):
    model = Plant
    fields = ['family', 'care']


class PlantDelete(DeleteView):
    model = Plant
    success_url = '/plants'


def add_watering(request, plant_id):
    form = WateringForm(request.POST)
    if form.is_valid():
        new_watering = form.save(commit=False)
        new_watering.plant_id = plant_id
        new_watering.save()

    return redirect('detail', plant_id=plant_id)


class GrowingMediaList(ListView):
    model = GrowingMedia


class GrowingMediaDetail(DetailView):
    model = GrowingMedia


class GrowingMediaCreate(CreateView):
    model = GrowingMedia
    fields = '__all__'


class GrowingMediaUpdate(UpdateView):
    model = GrowingMedia
    fields = '__all__'


class GrowingMediaDelete(DeleteView):
    model = GrowingMedia
    success_url = '/growing_med'


def assoc_growing_med(request, plant_id, growing_med_id):
    Plant.objects.get(id=plant_id).growing_media.add(growing_med_id)

    return redirect('detail', plant_id=plant_id)


def unassoc_growing_med(request, plant_id, growing_med_id):
    Plant.objects.get(id=plant_id).growing_media.remove(growing_med_id)

    return redirect('detail', plant_id=plant_id)


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