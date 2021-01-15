from rest_framework import serializers

from cmdb.models import Business, Host


class BusinessSerializer(serializers.ModelSerializer):
    '''
    业务序列化
    '''
    hosts = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Host.objects.all(),
                                               source='host_set', help_text='主机')

    class Meta:
        model = Business
        fields = ('id', 'name', 'use', 'network', 'login_url', 'username', 'password', 'desc', 'pid', 'hosts')
