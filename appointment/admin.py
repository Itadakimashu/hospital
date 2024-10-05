from typing import Any
from django.contrib import admin
from .models import Appointment

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['paitent','doctor','symptoms','time']

    def save_model(self, request, obj, form, change):
        if change:
            orginal_obj = self.model.objects.get(pk=obj.pk)
            if orginal_obj.cancel != obj.cancel and obj.cancel:
                obj.status = 'cancelled'
        
            if obj.status != orginal_obj.status and obj.status == 'running':
                pass #send Email
        
        super().save_model(request, obj, form, change)


admin.site.register(Appointment,AppointmentAdmin)