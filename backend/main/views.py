from django.shortcuts import render
from .models import *
from .serializers import *

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.core.exceptions import PermissionDenied
from django.db.models import Q

# Permite que apenas Coordenadores façam GET/POST/PUT/DELETE
# class DeadlineCustomPermission(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='Coodernadores').exists()

# Permite que apenas coordenadores façam POST/PUT/DELETE
# Mas libera o GET para os usuários autenticados
class DeadlineCustomPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.has_perm('main.view_deadline')
        return request.user.has_perms(['main.add_deadline', 'main.delete_deadline', 'main.change_deadline'])


class DeadlineView(ModelViewSet):
    queryset = Deadline.objects.all()
    serializer_class = DeadLineSerializer
    permission_classes = (DeadlineCustomPermission,)

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.groups.filter(name='Coordenadores').exists():
    #         return Deadline.objects.all()
    #     else:
    #         raise PermissionDenied()
