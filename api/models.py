from django.db import models
from django.core.exceptions import ValidationError


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    registration_id = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.registration_id})"


class Appointment(models.Model):
    # class TimeSlot(models.TextChoices):
    #     TIME_9AM = '9:00 AM', '9:00 AM'
    #     TIME_10AM = '10:00 AM', '10:00 AM'
    #     TIME_11AM = '11:00 AM', '11:00 AM'
    #     TIME_12PM = '12:00 PM', '12:00 PM'

    class Status(models.TextChoices):
        CONFIRMED = 'Confirmed', 'Confirmed'
        CANCELLED = 'Cancelled', 'Cancelled'

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient_name = models.CharField(max_length=100)
    date = models.DateField()
    time_slot = models.TimeField()
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



class DoctorAvailability(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = 'Monday', 'Monday'
        TUESDAY = 'Tuesday', 'Tuesday'
        WEDNESDAY = 'Wednesday', 'Wednesday'
        THURSDAY = 'Thursday', 'Thursday'
        FRIDAY = 'Friday', 'Friday'
        SATURDAY = 'Saturday', 'Saturday'
        SUNDAY = 'Sunday', 'Sunday'

    doctor = models.ForeignKey(
        'Doctor',
        on_delete=models.CASCADE,
        related_name='availabilities'
    )
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration = models.PositiveIntegerField(
        help_text="Duration in minutes (e.g., 15, 30, 60)"
    )

    def clean(self):
        #  Validation 1: start < end
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

        #  Validation 2: slot_duration > 0
        if self.slot_duration <= 0:
            raise ValidationError("Slot duration must be greater than 0.")

        #  Validation 3: Overlapping check
        overlapping = DoctorAvailability.objects.filter(
            doctor=self.doctor,
            day_of_week=self.day_of_week,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError("This availability overlaps with an existing one.")

    def __str__(self):
        return f"{self.doctor.name} - {self.day_of_week} ({self.start_time} to {self.end_time})"

