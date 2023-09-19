from django.shortcuts import render
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import login
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import status
from myauth.models import User 
from tutor.models import Booking
from .serializers import LoginSerializer, BookingSerializer, UserSerializer
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
    search_fields = ['first_name', 'last_name', 'email_address', 'user_uuid']
    filter_backends = (SearchFilter,)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['student', ]
    search_fields = ['$student__user__first_name', '$student__user__last_name', '$student__user__email_address', 'student__user__email_address']

