from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from myapp.models import User
from myapp.serializers import UserSerializer

@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user_level = data.get('user_level', 1)  

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        user = User(username=username, user_level=user_level)
        user.set_password(password) 
        user.save()

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_all_users(request):
    data=User.objects.all()
    serializer=UserSerializer(data,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)