from rest_framework.serializers import ModelSerializer
from base.models import User, Group, Task, Message


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'