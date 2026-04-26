from rest_framework import serializers
from .models import Doctor, Appointment
from typing import Dict, Any
from .utils.slot_utils import get_available_slots
from django.db import transaction, IntegrityError



class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'registration_id']
        read_only_fields = ['id']


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'doctor_name', 'patient_name', 'date', 'time_slot', 'status']
        read_only_fields = ['id', 'status']
        validators = []

    # # Custom validation to ensure doctor is available on the selected date.
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that the selected time slot is available for the doctor on the given date."""
        doctor = data['doctor']
        date = data['date']

        available_slots = get_available_slots(doctor, date)
        if not available_slots:
            raise serializers.ValidationError({
            "time_slot": f"Doctor is not available on this day {date}."
            })
        
        return data
    

    def create(self, validated_data):
        """Override create method to handle potential race conditions when booking appointments."""
        try:
            with transaction.atomic():
                appointment = Appointment.objects.create(**validated_data)
                return appointment
        except IntegrityError:
            raise serializers.ValidationError({
                "time_slot": "This slot has already been booked. Please choose another slot."
            })