# from django.contrib.auth.models import AbstractUser
# from django.db import models
# # from users.models import CustomUser

# class CustomUser(AbstractUser):
#     # You can add extra fields for the user, such as 'role'
#     ROLE_CHOICES = [
#         ('doctor', 'Doctor'),
#         ('patient', 'Patient'),
#         ('admin', 'Admin'),
#     ]
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

#     def __str__(self):
#         return self.username



# class Doctor(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
#     specialization = models.CharField(max_length=100)
#     experience_years = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"Dr. {self.user.username} ({self.specialization})"


# class Patient(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
#     doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
#     medical_history = models.TextField(blank=True)

#     def __str__(self):
#         return self.user.username

from django.contrib.auth.models import User
from django.db import models

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    role = models.CharField(max_length=10, choices=[('doctor', 'Doctor')], default='doctor')
    specialization = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialization})"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    role = models.CharField(max_length=10, choices=[('patient', 'Patient')], default='patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

