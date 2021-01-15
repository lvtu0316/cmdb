from rest_framework import serializers

from cmdb.models import Cabinet, Host


class CabinetSerializer(serializers.ModelSerializer):

    hosts = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Host.objects.all(), source='host_set')

    class Meta:
        model = Cabinet
        fields = '__all__'
