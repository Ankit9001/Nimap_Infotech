
from django.contrib import admin
from django.urls import path
from myapp.Logic_views.user_views import create_user,get_all_users
from myapp.Logic_views.client import client_list,client_list_create,manage_client
from myapp.Logic_views.project import create_project,project_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users', get_all_users, name='get_all_users'),
    path('api/create_user', create_user, name='create_user'),
    path('api/client_list', client_list, name='client_list'),
    path('api/client_list_create', client_list_create, name='client-list-create'),
    path('api/create_project', create_project, name='create_project'),
    path('api/clients/<int:id>', manage_client, name='manage_client'),
    path('api/projects', project_list, name='project_list'),  

]
