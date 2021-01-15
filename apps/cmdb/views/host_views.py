from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from pyexcel_xlsx import get_data

from cmdb.models import Host
from cmdb.serializer.host_serializer import HostSerializer, HostListSerializer, HostIPListSerializer
from common.common import CommonPagination, RbacPermission
from untitled2.basic import ApiResponse
from untitled2.status_code import BAD


class HostViewSet(ModelViewSet):
    """
    主机增删改查
    """
    perms_map = ({'*': 'admin'}, {'*': 'host_all'}, {'get': 'host_list'}, {'post': 'host_create'},
                 {'put': 'host_edit'}, {'delete': 'host_delete'}, {'patch': 'host_edit'},
                 {'get': 'group_list'}, {'get': 'cabinet_list'})
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('status', 'os_type', 'device_type', 'groups', 'businesses', 'labels', 'network_type')
    search_fields = ('ip',)
    ordering_fields = ('ip',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'list':
            return HostListSerializer
        return HostSerializer


class HostListView(ListAPIView):
    """
    主机IP列表
    """
    queryset = Host.objects.all()
    serializer_class = HostIPListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('ip',)
    ordering_fields = ('ip',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ImportExcelView(APIView):
    """
    导入Excel
    """
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.data["file"]
        data = get_data(file_obj)
        data_list = []
        header_cols = data['Sheet1'][1]
        rows = data['Sheet1']
        print(rows)
        for row in range(2, len(rows)):
            for col in range(len(rows[row])):
                Host(header_cols[col], rows[row][col]).save()

        #
        # serializer = HostSerializer(data=data_list, many=True)
        # if serializer.is_valid():
        #     Host.objects.bulk_create(data_list)
        #     return ApiResponse(data=data_list, status=201)
        # else:
        #     return ApiResponse(serializer.errors, status=BAD)




