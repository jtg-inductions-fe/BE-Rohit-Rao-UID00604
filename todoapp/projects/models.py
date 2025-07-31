from django.db import models
from django.conf import settings


class Project(models.Model):

    class Status(models.IntegerChoices):
        TO_BE_STARTED = 0, "To be started"
        IN_PROGRESS = 1, "In progress"
        COMPLETED = 2, "Completed"

    NAME_MAX_LENGTH = 100
    STATS_DEFAULT = 0
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ProjectMember")
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    max_members = models.PositiveIntegerField()
    status = models.IntegerField(choices=Status.choices, default=STATS_DEFAULT)

    def __str__(self) -> str:
        return self.name


class ProjectMember(models.Model):

    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("project", "member")

    def __str__(self):
        return (
            f"{self.project.name} - {self.member.get_full_name() or self.member.email}"
        )
