from rest_framework.viewsets import ModelViewSet
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Doctor, Appointment
from .serializers import DoctorSerializer, AppointmentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from .utils.slot_utils import get_available_slots
from django.db import transaction


class DoctorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Doctor.objects.all().order_by("name")
    serializer_class = DoctorSerializer

    # for available slots
    @action(detail=True, methods=['get'], url_path='available-slots')
    def available_slots(self, request, pk=None):
        doctor = self.get_object()
        date_str = request.query_params.get('date')

        if not date_str:
            return Response({"error": "date is required"}, status=400)

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format (YYYY-MM-DD)"}, status=400)

        slots = get_available_slots(doctor, date)

        formatted_slots = [slot.strftime("%H:%M") for slot in slots]

        return Response(formatted_slots)
    

class AppointmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.select_related('doctor').order_by("date", "time_slot")
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date']

    def get_queryset(self) -> QuerySet[Appointment]:
        return super().get_queryset()
    
    # for appointment cancellation
    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()

        # already cancelled check
        if appointment.status == Appointment.Status.CANCELLED:
            return Response(
                {"error": "Appointment already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment.status = Appointment.Status.CANCELLED
        appointment.save()

        return Response({"message": "Appointment cancelled successfully"})
        

    # for appointment rescheduling
    @action(detail=True, methods=['patch'])
    def reschedule(self, request, pk=None):
        appointment = self.get_object()

        #  already cancelled check
        if appointment.status == Appointment.Status.CANCELLED:
            return Response(
                {"error": "Cannot reschedule a cancelled appointment"},
                status=400
            )

        new_date = request.data.get("date")
        new_time_slot = request.data.get("time_slot")

        if not new_date or not new_time_slot:
            return Response({"error": "date and time_slot required"}, status=400)

        serializer = AppointmentSerializer(data={
            "doctor": appointment.doctor.id,
            "patient_name": appointment.patient_name,
            "date": new_date,
            "time_slot": new_time_slot
        })

        serializer.is_valid(raise_exception=True)

        # same slot check
        if (
            appointment.date == serializer.validated_data["date"]
            and appointment.time_slot == serializer.validated_data["time_slot"]
        ):
            return Response(
                {"error": "New slot must be different from current slot"},
                status=400
            )

        #  slot already booked
        if Appointment.objects.filter(
            doctor=appointment.doctor,
            date=serializer.validated_data["date"],
            time_slot=serializer.validated_data["time_slot"],
            status=Appointment.Status.CONFIRMED
        ).exclude(id=appointment.id).exists():
            return Response({"error": "Slot already booked"}, status=400)

        with transaction.atomic():
            appointment.status = Appointment.Status.CANCELLED
            appointment.save()

            new_appointment = serializer.save()

        return Response({
            "message": "Rescheduled successfully",
            "new_id": new_appointment.id
        })