from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.common.common import RbacPermission, CommonPagination
from ..models import Role
from ..serializer.role_serializer import RoleSerializer


class RoleViewSet(ModelViewSet):
    """
    角色管理增删改查
    """
    perms_map = ({'*': 'admin'}, {'*': 'role_all'}, {'get': 'role_list'}, {'post': 'role_create'}, {'put': 'role_edit'},
                 {'delete': 'role_delete'})
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)

