from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    registration_id = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.registration_id})"


class Appointment(models.Model):
    class TimeSlot(models.TextChoices):
        TIME_9AM = '9:00 AM', '9:00 AM'
        TIME_10AM = '10:00 AM', '10:00 AM'
        TIME_11AM = '11:00 AM', '11:00 AM'
        TIME_12PM = '12:00 PM', '12:00 PM'

    class Status(models.TextChoices):
        CONFIRMED = 'Confirmed', 'Confirmed'
        CANCELLED = 'Cancelled', 'Cancelled'

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient_name = models.CharField(max_length=100)
    date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TimeSlot.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONFIRMED)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'time_slot'],
                condition=models.Q(status='Confirmed'),
                name='unique_confirmed_slot'
            )
        ]

    def __str__(self) -> str:
        return f"{self.patient_name} - {self.doctor.name} on {self.date} at {self.time_slot}"