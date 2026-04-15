from rest_framework.viewsets import ModelViewSet
# from rest_framework.request import Request
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Doctor, Appointment
from .serializers import DoctorSerializer, AppointmentSerializer


class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all().order_by("name")
    serializer_class = DoctorSerializer


# class AppointmentViewSet(ModelViewSet):
#     queryset = Appointment.objects.select_related('doctor')
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         queryset = super().get_queryset().order_by("date", "time_slot")

#         doctor_id = self.request.query_params.get('doctor_id')
#         date = self.request.query_params.get('date')

#         if doctor_id:
#             queryset = queryset.filter(doctor_id=doctor_id)

#         if date:
#             queryset = queryset.filter(date=date)

#         return queryset

class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.select_related('doctor').order_by("date", "time_slot")
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date']

    def get_queryset(self) -> QuerySet[Appointment]:
        return super().get_queryset()