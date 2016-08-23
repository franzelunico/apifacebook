from django.contrib import admin
from .models import User, Location, School, TokenInfo

# Register your models here.
admin.site.register(User)
admin.site.register(Location)
admin.site.register(School)
admin.site.register(TokenInfo)
