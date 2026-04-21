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