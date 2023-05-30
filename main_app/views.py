from django.shortcuts import render

# Baby step:
plants = [
    {'name': 'Pothos', 'family': 'Araceae', 'care': 'Water every 1-2 weeks'},
    {'name': 'Zee Zee Plant', 'family': 'Araceae', 'care': 'Water every 3-4 weeks'}
]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def plants_index(request):
    return render(request, 'plants/index.html', {
        'plants': plants
    })
