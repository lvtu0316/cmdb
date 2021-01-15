import coreapi
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.views import exception_handler, APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rbac.models import Organization
from rbac.serializer.organization_serializer import OrganizationUserTreeSerializer
from .TreeSerializer import TreeSerializer
from untitled2.basic import ApiResponse


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        msg = '失败' if response.status_code >= 400 else '成功'
        notification_response = {}
        notification_response['code'] = response.status_code
        notification_response['message'] = msg
        notification_response['data'] = response.data
        response.data = notification_response
    return response


def DocParam(name="default", location="query",
             required=True, description=None, type="string",
             *args, **kwargs):
    return coreapi.Field(name=name, location=location,
                         required=required, description=description,
                         type=type)


class CommonPagination(PageNumberPagination):
    '''
    分页设置
    '''
    page_size = 10
    page_size_query_param = 'size'


class RbacPermission(BasePermission):
    '''
    自定义权限
    '''

    @classmethod
    def get_permission_from_role(self, request):
        try:
            perms = request.user.roles.values(
                'permissions__method',
            ).distinct()
            return [p['permissions__method'] for p in perms]
        except AttributeError:
            return None

    def has_permission(self, request, view):
        perms = self.get_permission_from_role(request)
        if perms:
            if 'admin' in perms:
                return True
            elif not hasattr(view, 'perms_map'):
                return True
            else:
                perms_map = view.perms_map
                _method = request._request.method.lower()
                for i in perms_map:
                    for method, alias in i.items():
                        if (_method == method or method == '*') and alias in perms:
                            return True


class TreeAPIView(ListAPIView):
    '''
    自定义树结构View
    '''
    serializer_class = TreeSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        tree_dict = {}
        tree_data = []
        try:
            for item in serializer.data:
                tree_dict[item['id']] = item
            for i in tree_dict:
                if tree_dict[i]['pid']:
                    pid = tree_dict[i]['pid']
                    parent = tree_dict[pid]
                    parent.setdefault('children', []).append(tree_dict[i])
                else:
                    tree_data.append(tree_dict[i])
            results = tree_data
        except KeyError:
            results = serializer.data
        if page is not None:
            return self.get_paginated_response(results)
        return ApiResponse(results)


class OrganizationUserTreeView(APIView):
    '''
    组织架构关联用户树
    '''
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        organizations = Organization.objects.all()
        serializer = OrganizationUserTreeSerializer(organizations, many=True)
        tree_dict = {}
        tree_data = []
        for item in serializer.data:
            new_item = {
                'id': 'o' + str(item['id']),
                'label': item['label'],
                'pid': item['pid'],
                'children': item['children']
            }
            tree_dict[item['id']] = new_item
        for i in tree_dict:
            if tree_dict[i]['pid']:
                pid = tree_dict[i]['pid']
                parent = tree_dict[pid]
                parent['children'].append(tree_dict[i])
            else:
                tree_data.append(tree_dict[i])
        return ApiResponse(tree_data)
