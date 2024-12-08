from django.shortcuts import render

# appointments/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AppointmentSerializer
from .models import Appointment


class AppointmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user)  # Automatically associate the logged-in user as the patient
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AppointmentListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.filter(patient=request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)