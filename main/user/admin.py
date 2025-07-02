from django.contrib import admin
from .models import CustomUser,TypeUser

admin.site.register(CustomUser)
admin.site.register(TypeUser)