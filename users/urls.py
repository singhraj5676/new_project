from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet
router = DefaultRouter()
router.register('doctors', DoctorViewSet, basename='doctor')
router.register('patients', PatientViewSet, basename='patient')

from .views import (
    # UserProfileView,
    # PasswordResetView,
    # PasswordResetConfirmView,
    RegisterView,
    LoginView,
    LogoutView,
)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),  # User registration
    path('login/', LoginView.as_view(), name='login'),  # User login
    path('logout/', LogoutView.as_view(), name='logout'),  # User logout
    # path('profile/', UserProfileView.as_view(), name='user-profile'),  # User profile
    # path('password-reset/', PasswordResetView.as_view(), name='password-reset'),  # Request password reset
    # path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),  # Confirm password reset
]
