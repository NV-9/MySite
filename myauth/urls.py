from django.urls import path 
from .views import *

urlpatterns = [
    path('', AuthRedirectView.as_view(), name = 'auth'),
    path('login/', AuthLoginView.as_view(), name = 'login'),
    path('logout/', AuthLogoutView.as_view(), name = 'logout'),
    path('signup/', AuthSignupView.as_view(), name = 'signup'),
    path('signup/<str:token>/', AuthSignupView.as_view(), name = 'signupverify'),
    path('profile/', AuthProfileView.as_view(), name = 'profile'),
    path('reset/', AuthPasswordRequestView.as_view(), name = 'reset'),
    path('reset/<str:token>/', AuthPasswordRequestView.as_view(), name = 'resetrequest'),
    path('resetpassword/<str:instance>/', AuthPasswordResetView.as_view(), name = 'resetpassword'),
]