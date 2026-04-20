from rest_framework.viewsets import ModelViewSet
# from rest_framework.request import Request
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Doctor, Appointment
from .serializers import DoctorSerializer, AppointmentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class DoctorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Doctor.objects.all().order_by("name")
    serializer_class = DoctorSerializer

class AppointmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.select_related('doctor').order_by("date", "time_slot")
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date']

    def get_queryset(self) -> QuerySet[Appointment]:
        return super().get_queryset()