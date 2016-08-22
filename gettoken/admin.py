from django.contrib import admin
from .models import User, Location, School, Concentration, Education

# Register your models here.
admin.site.register(User)
admin.site.register(Location)
admin.site.register(School)
admin.site.register(Concentration)
admin.site.register(Education)
