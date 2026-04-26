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
    booked_slots = set(Appointment.objects.filter(
        doctor=doctor,
        date=date,
        status=Appointment.Status.CONFIRMED
    ).values_list('time_slot', flat=True)
    )
    
    #  Step 5: Available slots filter
    available_slots = [slot for slot in all_slots if slot not in booked_slots]

    return sorted(available_slots)

def get_next_available_slot(doctor, date):
    slots = get_available_slots(doctor, date)
    return slots[0] if slots else None


def check_slot_and_suggest(doctor, date, time_slot, exclude_id=None):
    qs = Appointment.objects.filter(
        doctor=doctor,
        date=date,
        time_slot=time_slot,
        status=Appointment.Status.CONFIRMED
    )

    if exclude_id:
        qs = qs.exclude(id=exclude_id)

    if qs.exists():
        next_slot = get_next_available_slot(doctor, date)

        if next_slot:
            return {
                "error": "Slot already  booked",
                "next_available": next_slot.strftime("%H:%M")
            }

        return {
            "error": "No slots available for this day"
        }

    return None