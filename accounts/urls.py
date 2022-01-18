from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    # TokenVerifyView,
)
from .views import (
    ChangePasswordView,
    RegisterView,
    LogoutView,
    HelloView,

)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('hello/', HelloView.as_view(), name='hello'),

]
