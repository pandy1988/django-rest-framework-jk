from django.contrib import admin

from rest_framework_jk import models

# Register your models here.

admin.site.register(models.AuthKey)
admin.site.register(models.RefreshKey)
admin.site.register(models.AccessKey)
