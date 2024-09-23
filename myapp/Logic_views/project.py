from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from myapp.models import Client, Project, User
from myapp.serializers import ProjectSerializer, ProjectListSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    data = request.data
    client_id = data.get('client_id')
    users = data.get('users', [])

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=status.HTTP_400_BAD_REQUEST)

    user_instances = User.objects.filter(id__in=users)
    if not user_instances.exists():
        return Response({'error': 'Users not found'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ProjectSerializer(data=data)
    if serializer.is_valid():
        project = serializer.save(client=client, created_by=request.user)  
        project.users.set(user_instances)

        response_data = {
            'id': project.id,
            'project_name': project.project_name,
            'client': client.client_name,  
            'users': [{'id': user.id, 'name': user.username} for user in user_instances],
            'created_at': project.created_at,
            'created_by': project.created_by.username
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_list(request):
    projects = Project.objects.all()
    serializer = ProjectListSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
