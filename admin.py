from django.contrib import admin
from .models import Information as ProjectInformation
from .models import Task as ProjectTask

# Register your models here.
admin.site.register(ProjectInformation)
admin.site.register(ProjectTask)
