from django.contrib import admin
from .models import Doctor, Appointment, DoctorAvailability

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialization', 'registration_id']
    search_fields = ['name', 'specialization']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id','patient_name', 'doctor', 'date', 'time_slot', 'status']
    list_filter = ['date', 'status', 'doctor']
    search_fields = ['patient_name', 'doctor__name']

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time', 'slot_duration')
    list_filter = ['day_of_week', 'doctor']
    search_fields = ['doctor__name']