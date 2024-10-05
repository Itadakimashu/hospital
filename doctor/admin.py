from django.contrib import admin

from . import models

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug" : ['name',]
    }


admin.site.register(models.Designation,SlugAdmin)
admin.site.register(models.Specialization,SlugAdmin)
admin.site.register(models.AvailableTime)
admin.site.register(models.Doctor)
admin.site.register(models.Review)