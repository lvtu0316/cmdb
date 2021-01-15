from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from cmdb.models import Cabinet
from cmdb.serializer.cabinet_serializer import CabinetSerializer
from common.common import CommonPagination, RbacPermission


class CabinetViewSet(ModelViewSet):
    perms_map = (
        {'*': 'admin'}, {'*': 'cabinet_all'}, {'get': 'cabinet_list'}, {'post': 'cabinet_create'}, {'put': 'cabinet_edit'},
        {'delete': 'cabinet_delete'}, {'patch': 'cabinet_edit'}, {'get': 'host_list'})
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('num',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)


