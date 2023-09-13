from django.urls import path, include
from rest_framework import routers
from .views import LoginView, UserViewSet, BookingViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bookings', BookingViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
]