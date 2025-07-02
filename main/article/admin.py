from django.contrib import admin
from . import models 

admin.site.register(models.Article)
admin.site.register(models.Category)
admin.site.register(models.Function)
admin.site.register(models.Image)
admin.site.register(models.Shortcut)