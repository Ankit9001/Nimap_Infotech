
from rest_framework import serializers
from .models import User, Client, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  

class ClientSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()  

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by']
        read_only_fields = ['created_at']

    def get_projects(self, client):
        # Return the related projects as simple strings
        return client.projects.values_list('project_name', flat=True)

class ProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.client_name', read_only=True)
    users = UserSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name', 'users', 'created_at', 'created_by']

class ProjectListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.client_name', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name', 'created_at', 'created_by']
