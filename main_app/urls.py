from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('plants/', views.plants_index, name='index'),
    path('plants/<int:plant_id>/', views.plants_detail, name='detail'),
    path('plants/create/', views.PlantCreate.as_view(), name='plants_create'),
    path('plants/<int:pk>/update/', views.PlantUpdate.as_view(), name='plants_update'),
    path('plants/<int:pk>/delete/', views.PlantDelete.as_view(), name='plants_delete'),
    path('plants/<int:plant_id>/add_watering/', views.add_watering, name='add_watering'),
    path('plants/<int:plant_id>/assoc_growing_med/<int:growing_med_id>/', views.assoc_growing_med, name='assoc_growing_med'),
    path('growing_med/', views.GrowingMediaList.as_view(), name='growing_med_index'),
    path('growing_med/<int:pk>/', views.GrowingMediaDetail.as_view(), name='growing_med_detail'),
    path('growing_med/create/', views.GrowingMediaCreate.as_view(), name='growing_med_create'),
    path('growing_med/<int:pk>/update/', views.GrowingMediaUpdate.as_view(), name='growing_med_update'),
    path('growing_med/<int:pk>/delete/', views.GrowingMediaDelete.as_view(), name='growing_med_delete'),
]


