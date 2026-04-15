from django.contrib import admin
from .models import Doctor, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'registration_id']
    search_fields = ['name', 'specialization']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor', 'date', 'time_slot', 'status']
    list_filter = ['date', 'status', 'doctor']
    search_fields = ['patient_name', 'doctor__name']