from django.urls import path
from .views import ProjectMemberApiViewSet

project_member = ProjectMemberApiViewSet.as_view({
    'post': 'create',
    'put': 'update',
})

urlpatterns = [
    path('<int:project_pk>/', project_member, name='project-members'),
]