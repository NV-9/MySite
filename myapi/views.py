from django.shortcuts import render
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import login
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import status
from myauth.models import User 
from mytutor.models import Booking, Student, Lesson
from .serializers import LoginSerializer, BookingSerializer, UserSerializer, StudentSerializer, LessonSerializer
from rest_framework import viewsets


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data, context = {'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status = status.HTTP_202_ACCEPTED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = UserSerializer.Meta.fields
    filter_backends = [DjangoFilterBackend, SearchFilter]
    
    def get_queryset(self):
        queryset = super().get_queryset()

        ids = self.request.query_params.get('ids', None)
        if ids:
            ids_list = ids.split(',')
            queryset = queryset.filter(id__in=ids_list)

        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['student', ]
    search_fields = ['$student__user__first_name', '$student__user__last_name', '$student__user__email_address', 'student__user__email_address']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user', ]
    search_fields = ['$student__user__first_name', '$student__user__last_name', '$student__user__email_address', 'student__user__email_address']


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['lessonplan', 'start_time', 'end_time', 'clash', 'paid']
    search_fields = ['start_time', 'end_time']

    def get_queryset(self):
        queryset = super().get_queryset()

        ids = self.request.query_params.get('lessons', None)
        if ids:
            ids_list = ids.split(',')
            queryset = queryset.filter(lessonplan__student__user__id__in=ids_list)

        return queryset

