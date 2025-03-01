from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Todo
from .serializers import UserSerializer, TodoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_completed']
    search_fields = ['title', 'description']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Todo.objects.filter(user=self.request.user)
        return Todo.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def destroy(self, request, pk=None):  # Удаление по ID
        try:
            todo = Todo.objects.get(id=pk, user=request.user)
            todo.delete()
            return Response({"message": "Задача удалена"}, status=status.HTTP_204_NO_CONTENT)
        except Todo.DoesNotExist:
            return Response({"error": "Задача не найдена"}, status=status.HTTP_404_NOT_FOUND)


class DeleteAllTodosViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request):
        Todo.objects.filter(user=request.user).delete()
        return Response({"message": "Все задачи удалены"})