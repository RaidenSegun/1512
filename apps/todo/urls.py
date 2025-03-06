from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.todo.views import TodoMixin, UserMixin

router = DefaultRouter()
router.register(r'todos', TodoMixin, basename="todos")
router.register(r'users', UserMixin, basename="users")

urlpatterns = [
    path('api/', include(router.urls)),  # <-- Префикс API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
