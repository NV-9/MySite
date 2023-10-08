from django.urls import path, include
from rest_framework import routers
from .views import LoginView, UserViewSet, BookingViewSet, StudentViewSet, LessonViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'students', StudentViewSet)
router.register(r'lessons', LessonViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
]