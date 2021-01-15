from rest_framework import serializers

from cmdb.models import Host


class HostSerializer(serializers.ModelSerializer):
    """
    主机详情
    """
    class Meta:
        model = Host
        fields = '__all__'


class HostListSerializer(serializers.ModelSerializer):
    """
    主机列表序列化

    """
    class Meta:
        model = Host
        fields = ('id', 'name', 'ip', 'device_type', 'network_type', 'businesses', 'os_version', 'status', 'groups',
                  'labels', 'warranty_date', 'cabinet')
        depth = 1


class HostIPListSerializer(serializers.ModelSerializer):
    """
    主机IP列表
    """
    id = serializers.IntegerField()
    ip = serializers.CharField(source='IP')
