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

    # Custom validation to prevent double booking
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that the selected time slot is available for the doctor on the given date."""
        doctor = data['doctor']
        date = data['date']
        time_slot = data['time_slot']

        available_slots = get_available_slots(doctor, date)
        if not available_slots:
            raise serializers.ValidationError({
            "time_slot": "Doctor is not available on this day."
            })
        
        if time_slot not in available_slots:
            raise serializers.ValidationError({
                "time_slot": "This slot is not available."
            })

        if Appointment.objects.filter(
            doctor=doctor,
            date=date,
            time_slot=time_slot,
            status=Appointment.Status.CONFIRMED
        ).exists():
            raise serializers.ValidationError({
                "time_slot": f"Doctor {doctor.name} already has an appointment at {time_slot} on {date}."
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