from django.urls import path,include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from ..views import userViews



urlpatterns = [


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', userViews.register_user, name='register'),
    path('profile/', userViews.getUserProfile, name='user-profile'),
    path('profile/update/', userViews.updateUserProfile, name='update-profile'),


] 
