from rest_framework import serializers

from cmdb.models import Label, Host


class LabelSerializer(serializers.ModelSerializer):
    hosts = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Host.objects.all(),
                                               source='host_set')

    class Meta:
        model = Label
        fields = '__all__'
