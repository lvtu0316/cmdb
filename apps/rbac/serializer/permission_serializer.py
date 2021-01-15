from rest_framework import serializers

from rbac.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    '''
    权限序列化
    '''
    menuname = serializers.ReadOnlyField(source='menus.name')

    class Meta:
        model = Permission
        fields = ('id','name','method','menuname','pid')
