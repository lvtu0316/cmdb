from rest_framework import serializers

from cmdb.models import DeviceGroup, Host


class DeviceGroupSerializer(serializers.ModelSerializer):
    hosts = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Host.objects.all(),
                                               source='host_set', help_text='主机')
    class Meta:
        model =DeviceGroup
        fields = "__all__"
