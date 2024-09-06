from rest_framework import serializers
from .models import Organization, MetaTable, MetaColumn

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'  


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaTable
        fields = '__all__'

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaColumn
        fields = '__all__'