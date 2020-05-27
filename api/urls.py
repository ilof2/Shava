from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from api.views import CreateOrder

urlpatterns = [
    path('auth/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('order/create/', CreateOrder.as_view(), name='create_order')
]

