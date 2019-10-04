from rest_framework import serializers

from connection.models import Connection


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ('survivor', 'advocate')
