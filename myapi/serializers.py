from django.contrib.auth import authenticate
from rest_framework import permissions, serializers
from myauth.models import User
from tutor.models import Booking


class LoginSerializer(serializers.Serializer):

    email_address = serializers.CharField(
        label = "Email Address",
        write_only = True
    )

    password = serializers.CharField(
        label = "Password",
        style = {'input_type': 'password'},
        trim_whitespace = False,
        write_only = True
    )

    def validate(self, attrs):
        username = attrs.get('email_address')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_uuid', 'email_address', 'date_of_birth', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_verified', 'created_at', 'updated_at']
        permission_classes = [permissions.IsAuthenticated]


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['student', 'start_time', 'end_time']
        permission_classes = [permissions.IsAuthenticated]

