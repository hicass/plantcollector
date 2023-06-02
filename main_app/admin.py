from django.contrib import admin
from .models import Plant, Watering, GrowingMedia, Photo

admin.site.register(Plant)
admin.site.register(Watering)
admin.site.register(GrowingMedia)
admin.site.register(Photo)

