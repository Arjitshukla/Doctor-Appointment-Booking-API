from rest_framework import serializers
from .models import Doctor, Appointment
from typing import Dict, Any


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
        doctor = data['doctor']
        date = data['date']
        time_slot = data['time_slot']

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