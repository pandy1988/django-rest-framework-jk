from django.contrib import admin

from rest_framework_jk.models import AuthKey, RefreshKey, AccessKey

# Register your models here.

admin.site.register(AuthKey)
admin.site.register(RefreshKey)
admin.site.register(AccessKey)
