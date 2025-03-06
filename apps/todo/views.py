from rest_framework import mixins, viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from apps.todo.models import Todo
from rest_framework.exceptions import PermissionDenied 
from apps.todo.serializers import TodoSerializer, UserSerializer

User = get_user_model()

class BaseMixin(viewsets.GenericViewSet,
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin):
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

class TodoMixin(BaseMixin):
    """Mixin для управления задачами"""
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ограничиваем доступ

    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Фильтруем задачи: обычный пользователь видит только свои"""
        user = self.request.user
        if user.is_staff:  # Админ видит всё
            return Todo.objects.all()
        return Todo.objects.filter(user=user)

    def perform_create(self, serializer):
        """Привязываем задачу к текущему пользователю, но даём возможность админам указывать ID"""
        if self.request.user.is_staff and 'user' in self.request.data:
            serializer.save()  # Админ может назначить пользователя
        else:
            serializer.save(user=self.request.user)  # Обычный юзер создаёт только для себя

    def perform_destroy(self, instance):
        """Обычные пользователи удаляют только свои задачи, админ может удалить любую"""
        user = self.request.user
        if user.is_staff or instance.user == user:
            instance.delete()
        else:
            raise PermissionDenied("Вы не можете удалить эту задачу.")  # Теперь без ошибок! 🚀


class UserMixin(BaseMixin):
    """Mixin для управления пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    search_fields = ['username', 'phone_number']
    ordering_fields = ['created_at']
    ordering = ['-created_at']




