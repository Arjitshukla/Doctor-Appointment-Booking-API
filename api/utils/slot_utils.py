from datetime import datetime, timedelta
from ..models import DoctorAvailability, Appointment


def get_available_slots(doctor, date):
    #  Step 1: Day 
    day_of_week = date.strftime('%A')

    #  Step 2: Availability fetch
    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor,
        day_of_week=day_of_week
    )

    all_slots = []

    #  Step 3: Slots generate 
    for availability in availabilities:
        start_time = availability.start_time
        end_time = availability.end_time
        duration = availability.slot_duration

        # datetime me convert
        current = datetime.combine(date, start_time)
        end = datetime.combine(date, end_time)

        while current < end:
            all_slots.append(current.time())
            current += timedelta(minutes=duration)

    #  Step 4: Booked slots fetch
    booked_slots = Appointment.objects.filter(
        doctor=doctor,
        date=date,
        status='Confirmed'
    ).values_list('time_slot', flat=True)

    booked_slots = set(booked_slots)

    #  Step 5: Available slots filter
    available_slots = [slot for slot in all_slots if slot not in booked_slots]

    return available_slots