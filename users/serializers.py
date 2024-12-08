from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import  Doctor, Patient

# users/serializers.py
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Doctor, Patient


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['doctor', 'patient'])

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

   

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Role-specific creation
        if role == 'doctor':
            Doctor.objects.create(
                user=user,
                specialization=self.initial_data.get('specialization'),
                experience_years=self.initial_data.get('experience_years', 0)
            )
        elif role == 'patient':
            # Associate patient with a doctor, if specified
            doctor_username = self.initial_data.get('doctor_username')
            doctor = Doctor.objects.filter(user__username=doctor_username).first()
            Patient.objects.create(
                user=user,
                doctor=doctor,
                medical_history=self.initial_data.get('medical_history', "")
            )

        return user


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        # Infer role based on related models
        role = None
        if hasattr(user, 'doctor_profile'):
            role = 'doctor'
        elif hasattr(user, 'patient_profile'):
            role = 'patient'
        else:
            raise serializers.ValidationError("No role associated with this user.")

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access['role'] = role  # Add role to the access token

        return {
            'refresh_token': str(refresh),
            'access': str(access),
            'role': role,
        }


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'specialization', 'experience_years']

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        user = User.objects.create(**user_data) if user_data else None
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

    def update(self, instance, validated_data):
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.experience_years = validated_data.get('experience_years', instance.experience_years)
        instance.save()
        return instance


class PatientSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'doctor', 'medical_history']

    def create(self, validated_data):
        doctor_data = validated_data.pop('doctor', None)
        doctor = Doctor.objects.create(**doctor_data) if doctor_data else None
        patient = Patient.objects.create(doctor=doctor, **validated_data)
        return patient

    def update(self, instance, validated_data):
        doctor_data = validated_data.pop('doctor', None)
        if doctor_data:
            DoctorSerializer(instance.doctor).update(instance.doctor, doctor_data)
        instance.medical_history = validated_data.get('medical_history', instance.medical_history)
        instance.save()
        return instance


  