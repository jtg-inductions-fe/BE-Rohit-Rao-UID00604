from django.urls import reverse
from rest_framework.test import APITestCase


class ProjectMemberAPIViewTestCase(APITestCase):

    def test_project_by_adding_users(self):
        user_data = {"user_ids": ["1", "2"]}
        response = self.client.post("/api/projects/1/", user_data)
        print(response.content)
        self.assertEqual(404, response.status_code)
