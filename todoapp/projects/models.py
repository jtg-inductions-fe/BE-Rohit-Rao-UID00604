
from django.db import models
from django.conf import settings

class Project(models.Model):

    STATUS_CHOICES = [
        (0, 'To be started'),
        (1, 'In progress'),
        (2, 'Completed'),
    ]

    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100)
    max_members = models.PositiveIntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self) -> str:
        return self.name
    
class ProjectMember(models.Model):

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project', 'member')

    def __str__(self):
        return f"{self.project.name} - {self.member.get_full_name() or self.member.email}"


