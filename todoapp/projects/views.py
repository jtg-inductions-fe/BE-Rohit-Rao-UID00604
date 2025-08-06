from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from projects import models as projects_models, serializers as projects_serializers


class ProjectMemberApiViewSet(ViewSet):
    """
    constraints
      - a user can be a member of max 2 projects only
      - a project can have at max N members defined in database for each project
    functionalities
    - add users to projects

      Request
      { user_ids: [1,2,...n] }
      Response
      {
        logs: {
          <user_id>: <status messages>
        }
      }
      following are the possible status messages
      case1: if user is added successfully then - "Member added Successfully"
      case2: if user is already a member then - "User is already a Member"
      case3: if user is already added to 2 projects - "Cannot add as User is a member in two projects"

      there will be many other cases think of that

    - update to remove users from projects

      Request
      { user_ids: [1,2,...n] }

      Response
      {
        logs: {
          <user_id>: <status messages>
        }
      }

      there will be many other cases think of that and share on forum
    """

    def get_project(self):
        return projects_models.Project.objects.get(pk=self.kwargs["project_pk"])

    def create(self, request, *args, **kwargs):
        try:
            project = self.get_project()
        except:
            raise Http404("Project does't exist")
        serializer = projects_serializers.ProjectMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logs = serializer.add_members(project)
        return Response({"logs": logs}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            project = self.get_project()
        except:
            raise Http404("Project does't exist")
        serializer = projects_serializers.ProjectMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logs = serializer.remove_members(project)
        return Response({"logs": logs}, status=status.HTTP_200_OK)
