from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import User, Task, Group, Message


@api_view(['GET'])
def index(request):
    data = {
        'users': User.objects.count(),
        'tasks': Task.objects.count(),
        'groups': Group.objects.count(),
        'messages': Message.objects.count(),
    }
    return Response(data)