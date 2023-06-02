from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Plant, GrowingMedia
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
    watering_form = WateringForm()

    return render(request, 'plants/detail.html', {
        'plant': plant,
        'watering_form': watering_form
    })

class PlantCreate(CreateView):
    model = Plant
    fields = '__all__'

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