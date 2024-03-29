from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    registrationNumber = models.CharField(max_length=30)
    phoneNimber = models.CharField(max_length=15, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' # Substitui o login com Username por login com Email
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


BLOCKS = [
    ('A', 'Bloco A'),
    ('B', 'Bloco B'),
    ('C', 'Bloco C')
]

TASK_TYPES = []

FILE_TYPES = [
    ('D', 'Documento'),
    ('F', 'Foto')
]

TASK_STATUS = [
    ('AB', 'Aberto'),
    ('EA', 'Em Andamento'),
    ('CA', 'Cancelado'),
    ('CO', 'Concluído'),
    ('EN', 'Encerrado')
]

class Environments(models.Model):
    name = models.CharField(max_length=100)
    block = models.CharField(max_length=30, choices=BLOCKS)

    def __str__(self):
        return self.name

class Tasks(models.Model):
    environmentFK = models.ForeignKey(Environments, related_name='tasksEnvironments', on_delete=models.CASCADE)
    reporterFK = models.ForeignKey(CustomUser, related_name='tasksCustomUser', on_delete=models.CASCADE)
    creationDate = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    diagnostic = models.CharField(max_length=250)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=TASK_STATUS)
    environmentAlocationFK = models.ForeignKey(EnvironmentAlocation, related_name='tasksEnvironmentAlocation', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class TasksAssignees(models.Model):
    taskFK = models.ForeignKey('Tasks', related_name='title', on_delete=models.CASCADE)
    assigneeFK = models.ForeignKey('CustomUser', related_name='email', on_delete=models.CASCADE)

    def __str__(self):
        return self.taskFK.title

class Equipments(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    assigneeFK = models.ForeignKey(CustomUser, related_name='equipmentsCustomUser', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
    
class TaskStatus(models.Model):
    taskFK = models.ForeignKey(Tasks, related_name='tasksAssigneesTask', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=TASK_STATUS)
    creationDate = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=300)

    def __str__(self):
        return self.taskFK.title

class TasksEquipments(models.Model):
    taskFK = models.ForeignKey(Tasks, related_name='tasksEquipmentsTask', on_delete=models.CASCADE)
    equipmentFK = models.ForeignKey(Equipments, related_name='equipmentsTask', on_delete=models.CASCADE)

    def __str__(self):
        return self.taskFK.title

class FilesTaskStatus(models.Model):
    taskStatusFK = models.ForeignKey(TaskStatus, related_name='statusTaskFiles', on_delete=models.CASCADE)
    link = models.CharField(max_length=2000)
    fileType = models.CharField(max_length=300, choices=FILE_TYPES)

    def __str__(self):
        return self.fileType
    
class EnvironmentsAssignees(models.Model):
    environmentFK = models.ForeignKey(Environments, related_name='environmentsAssigneesEnvironment', on_delete=models.CASCADE)
    assigneeFK = models.ForeignKey(CustomUser, related_name='environmentsAssigneesCustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.environmentFK.name
