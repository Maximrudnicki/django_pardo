from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    # path('api/v1/', include('djoser.urls.jwt')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/vocab/', include('vocab.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Проверка токена
    path('api/v1/accounts/', include('accounts.urls')),
]
