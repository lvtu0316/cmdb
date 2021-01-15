from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from rbac.models import Permission
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from common.common import CommonPagination, RbacPermission, TreeAPIView
from rbac.serializer.permission_serializer import PermissionSerializer


class PermissionViewSet(ModelViewSet, TreeAPIView):
    '''
    权限：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'permission_all'}, {'get': 'permission_list'}, {'post': 'permission_create'},
                 {'put': 'permission_edit'},{'delete': 'permission_delete'})
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)


class PermissionTreeView(TreeAPIView):
    '''
    权限树
    '''
    queryset = Permission.objects.all()
