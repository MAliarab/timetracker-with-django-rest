from django.contrib import admin
from record import models
# Register your models here.
admin.site.register(models.Project)
admin.site.register(models.Time)
admin.site.register(models.ProjectUser)