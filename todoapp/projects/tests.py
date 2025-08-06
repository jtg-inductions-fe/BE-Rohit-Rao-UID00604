import json

from rest_framework.test import APITestCase
from projects import models as projects_models
from users import models as users_models


class ProjectMemberAPIViewTestCase(APITestCase):
    fixtures = [
        "fixtures/01_data_dump.json",
    ]

    def setUp(self):
        self.user = users_models.CustomUser(
            first_name="dummy", last_name="my_strong_pass", email="test@email.com"
        )
        self.user2 = users_models.CustomUser(
            first_name="dummy2", last_name="my_strong_pass", email="test2@email.com"
        )
        self.project = projects_models.Project(name="test", max_members=5)
        self.user.save()
        self.user2.save()
        self.project.save()
        self.project.members.add(self.user)

    def test_project_by_adding_existing_users(self):
        data = {"user_ids": [f"{self.user.id}"]}
        output = {"logs": {f"{self.user.id}": "User is already a Member"}}

        response = self.client.post(f"/api/projects/{self.project.id}/", data)
        self.assertEqual(output, json.loads(response.content))

    def test_projects_by_adding_new_member(self):
        data = {"user_ids": [f"{self.user2.id}"]}
        output = {"logs": {f"{self.user2.id}": "Member added Successfully"}}

        response = self.client.post(f"/api/projects/{self.project.id}/", data)
        self.assertEqual(output, json.loads(response.content))

    def test_project_by_adding_user_in_more_than_two_project(self):
        data = {"user_ids": ["1"]}
        output = {"logs": {"1": "Cannot add as User is a member in two projects"}}

        response = self.client.post("/api/projects/1/", data)
        self.assertEqual(output, json.loads(response.content))

    def test_project_by_adding_wrong_user(self):
        data = {"user_ids": ["10000"]}
        output = {"logs": {"10000": "User does not exist"}}

        response = self.client.post("/api/projects/2/", data)
        self.assertEqual(output, json.loads(response.content))

    def test_project_by_adding_user_in_wrong_project(self):
        data = {"user_ids": ["1"]}

        response = self.client.post("/api/projects/2000/", data)
        self.assertEqual(404, response.status_code)

    def test_project_by_removing_existing_user(self):
        data = {"user_ids": [f"{self.user.id}"]}
        output = {"logs": {f"{self.user.id}": "User removed successfully"}}

        response = self.client.put(f"/api/projects/{self.project.id}/", data)

        self.assertEqual(output, json.loads(response.content))

    def test_project_by_removing_non_existing_user(self):
        data = {"user_ids": ["1"]}
        output = {"logs": {"1": "User is not a member of this project"}}

        response = self.client.put(f"/api/projects/1/", data)
        self.assertEqual(output, json.loads(response.content))
