from rest_framework import serializers
from apps.todo.models import User, Todo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'created_at', 'age']


# class TodoSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Todo
#         fields = ['id', 'title', 'description', 'is_completed', 'created_at', 'image', 'user']
#         read_only_fields = ['created_at']
#         # read_only_fields = ['user']


class TodoSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, source="user"
    )

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'is_completed', 'image', 'user_id']  # Добавили `user_id`
        read_only_fields = ['user']  # Обычные пользователи не могут менять `user`

    def validate(self, data):
        """Ограничение на указание user_id"""
        request = self.context['request']
        if not request.user.is_staff and 'user' in data:
            raise serializers.ValidationError("Вы не можете назначать задачи другим пользователям.")
        return data