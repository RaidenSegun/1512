from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.todo.views import UserViewSet, TodoViewSet, DeleteAllTodosViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'todos', TodoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('delete_todos/', DeleteAllTodosViewSet.as_view({'delete': 'destroy'}), name="delete_all_todos"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]