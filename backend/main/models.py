from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .manager import *


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

    objects = CustomManager()

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

COURSE_CATEGORY = [
    ('CAI', 'Curso de Aprendizagem Industrial'),
    ('CT', 'Curso Técnico'),
    ('CST', 'Curso Superior de Tecnologia'),
    ('FIC', 'Formação Continuada')
]

COURSE_DURATION_TYPE = [
    ('HRS', 'Horas'),
    ('SM', 'Semestre')
]

COURSE_AREA = [
    ('TI', 'Tecnologia da Informação'),
    ('MEC', 'Mecânica'),
    ('ELÉTR.', 'Elétrica')
]

COURSE_MODALITY = [
    ('EAD', 'Aulas Remotas'),
    ('P', 'Presencial'),
    ('HB', 'Híbrido')
]

TEACHER_ALOCATION_STATUS = [
    ('A', 'Assinalado'),
    ('C', 'Concluído'),
    ('R', 'Rascunho')
]

WEEK_DAYS = [
    ('DOM', 'Domingo'),
    ('SEG', 'Segunda-Feira'),
    ('TER', 'Terça-Feira'),
    ('QUA', 'Quarta-Feira'),
    ('QUI', 'Quinta-Feira'),
    ('SEX', 'Sexta-Feira'),
    ('SAB', 'Sábado')
]

PLAN_STATUS = [
    ('P', 'Pendente'),
    ('EA', 'Em Aprovação'),
    ('A' 'Aprovado'),
    ('ER', 'Em Revisão'),
    ('C', 'Cancelado')

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
    # environmentAlocationFK = models.ForeignKey(EnvironmentAlocation, related_name='tasksEnvironmentAlocation', on_delete=models.CASCADE)

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
    taskFK = models.ForeignKey(Tasks, related_name='tasksTaskStatusAssigneesTask', on_delete=models.CASCADE)
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

class Themes(models.Model):
    name = models.CharField(max_length=250)
    timeLoad = models.IntegerField()

    def __str__(self):
        return self.name

class Courses(models.Model):
    name = models.CharField(max_length=250)
    category = models.CharField(max_length=100, choices=COURSE_CATEGORY)
    duration = models.IntegerField()
    duration_type = models.CharField(max_length=100, choices=COURSE_DURATION_TYPE)
    area = models.CharField(max_length=100, choices=COURSE_DURATION_TYPE)
    modality = models.CharField(max_length=100, choices=COURSE_MODALITY)
    # themes = models.ManyToManyField(Themes)

    def __str__(self):
        return self.name

class CoursesThemes(models.Model):
    courseFK = models.ForeignKey(Courses, related_name='CoursesThemesCourse', on_delete=models.CASCADE)
    themeFK = models.ForeignKey(Themes, related_name='CoursesThemesTheme', on_delete=models.CASCADE)

    def __str__(self):
        return self.courseFK.name

class Classes(models.Model):
    courseFK = models.ForeignKey(Courses, related_name='ClassCourse', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return self.name

class ClassDivisions(models.Model):
    classFK = models.ForeignKey(Classes, related_name='ClassesDivisionClass', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class TeacherAlocation(models.Model):
    classFK = models.ForeignKey(Classes, related_name='TeacherAlocationClass', on_delete=models.CASCADE)
    themeFK = models.ForeignKey(Themes, related_name='TeacherAlocationTheme', on_delete=models.CASCADE)
    reporterFK = models.ForeignKey(CustomUser, related_name='TeacherAlocationReporter', on_delete=models.CASCADE)

    def __str__(self):
        return self.reporterFK.email

class TeacherAlocationDetail(models.Model):
    customUserFK = models.ForeignKey(CustomUser, related_name='TeacherAlocationDetailCustomUser', on_delete=models.CASCADE)
    classDivisionFK = models.ForeignKey(ClassDivisions, related_name='TeacherAlocationDetailClassDivision', on_delete=models.CASCADE)
    alocationStatus = models.CharField(max_length=100, choices=TEACHER_ALOCATION_STATUS)
    creationDate = models.DateField(auto_now_add=True)
    updatedDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.classDivisionFK.name

class TeacherAlocationDetailEnv(models.Model):
    environmentFK = models.ForeignKey(Environments, related_name='TeacherAlocationDetailEnvEnvironment', on_delete=models.CASCADE)
    teacherAlocationDetailFK = models.ForeignKey(Classes, related_name='TeacherAlocationDetailEnvTeacherAlocationDetail', on_delete=models.CASCADE)
    weekDay = models.CharField(max_length=100, choices=WEEK_DAYS)
    hourStart = models.TimeField()
    hourEnd = models.TimeField()
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return self.environmentFK.name

class Deadline(models.Model):
    targetDate = models.DateField()
    category = models.CharField(max_length=100, choices=COURSE_CATEGORY)

    def __str__(self):
        return self.category

class Signatures(models.Model):
    customUserFK = models.ForeignKey(CustomUser, related_name='SignaturesCustomUser', on_delete=models.CASCADE)
    signature = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.signature

class Plan(models.Model):
    customUserFK = models.ForeignKey(CustomUser, related_name='PlanCustomUser', on_delete=models.CASCADE)
    courseThemeFK = models.ForeignKey(CoursesThemes, related_name='PlanCourseTheme', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=PLAN_STATUS, default='P')
    signatureFK = models.ForeignKey(Signatures, related_name='PlanSignature', on_delete=models.CASCADE, blank=True, null=True)
    approverFK = models.ForeignKey(CustomUser, related_name='PlanApprover', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.customUserFK.email

class PlanStatus(models.Model):
    planFK = models.ForeignKey(Plan, related_name='PlanStatusPlan', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=PLAN_STATUS)
    comment = models.CharField(max_length=500)
    file = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.planFK.customUserFK.email

