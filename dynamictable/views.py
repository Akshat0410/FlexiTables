from django.shortcuts import render

from rest_framework import viewsets
from .models import Organization, MetaTable, MetaColumn
from .serializers import OrganizationSerializer, TableSerializer, ColumnSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import connections, connection

class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    def retrieve(self, request, pk=None):
        org = get_object_or_404(Organization, pk=pk)
        return Response(OrganizationSerializer(org).data)
    
    def create(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            org = serializer.save()
            self.create_database_for_org(org)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, pk=None):
        org = get_object_or_404(Organization, pk=pk)
        schema_name = f'org_{org.org_id}'
        with connection.cursor() as cursor:
            cursor.execute(f'DROP SCHEMA {schema_name} CASCADE')
        org.delete()
        return Response(status=204)

    def create_database_for_org(self, org: Organization):
        schema_name = f'org_{org.org_id}'
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE SCHEMA {schema_name}')


class TableViewSet(viewsets.ModelViewSet):
    serializer_class = TableSerializer
    queryset = MetaTable.objects.all()

    def create_dynamic_model(self, table: MetaTable, schema_name: str):
        model_name = table.name
        from django.db import models
        DynamicModel = type(model_name, (models.Model,), {
            '__module__': 'dynamictable.models',
            'Meta': type('Meta', (), {
                'db_table': f'"{schema_name}"."{model_name}"'  # Ensure schema and table name are quoted
            })
        })
        return DynamicModel
    def create_table(self, model):
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)

    def create(self, request, org_id):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            table = serializer.save()
            org = get_object_or_404(Organization, pk=org_id)
            schema_name = f'org_{org.org_id}'
            dynamic_model = self.create_dynamic_model(table, schema_name)
            self.create_table(dynamic_model)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def list(self, request, org_id):
        tables = MetaTable.objects.filter(organization=org_id)
        return Response(TableSerializer(tables, many=True).data)

    def retrieve(self, request, org_id, pk=None):
        table = get_object_or_404(MetaTable, pk=pk)
        serializer = TableSerializer(table)
        return Response(serializer.data)
    
    def destroy(self, request, org_id, pk=None):
        table = get_object_or_404(MetaTable, pk=pk)
        org = get_object_or_404(Organization, pk=org_id)
        schema_name = f'org_{org.org_id}'
        model = self.create_dynamic_model(table, schema_name)
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(model)
        table.delete()
        return Response(status=204)


class ColumnViewSet(viewsets.ModelViewSet):
    serializer_class = ColumnSerializer
    queryset = MetaColumn.objects.all()

    def get_field_by_type(self, column_name, column_type):
        from django.db import models
        field_mapping = {
            'CharField': models.CharField,
            'IntegerField': models.IntegerField,
            'BooleanField': models.BooleanField,
        }
        field_class = field_mapping.get(column_type)
        if field_class:
            return field_class(max_length=255 if column_type == 'CharField' else None, name=column_name)
        return None

    def create(self, request, org_id, table_id):
        serializer = ColumnSerializer(data=request.data)
        if serializer.is_valid():
            column = serializer.save()
            table = get_object_or_404(MetaTable, pk=table_id)
            org = table.organization
            schema_name = f'org_{org.org_id}'
            column_name = column.name
            column_type = column.data_type

            # Dynamically add the column to the model
            with connection.schema_editor() as schema_editor:
                model = self.create_dynamic_model(table, schema_name)
                field = self.get_field_by_type(column_name, column_type)
                if field:
                    model.add_to_class(column_name, field)
                    schema_editor.add_field(model, field)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def list(self, request, org_id, table_id):
        tables = MetaColumn.objects.filter(table_id=table_id)
        return Response(ColumnSerializer(tables, many=True).data)
    
    def create_dynamic_model(self, table: MetaTable, schema_name: str):
        model_name = table.name
        from django.db import models
        DynamicModel = type(model_name, (models.Model,), {
            '__module__': 'dynamictable.models',
            'Meta': type('Meta', (), {
                'db_table': f'"{schema_name}"."{model_name}"'  # Ensure schema and table name are quoted
            })
        })
        return DynamicModel
    
    def destroy(self, request, org_id, table_id, pk=None):
        column = get_object_or_404(MetaColumn, pk=pk)
        table = get_object_or_404(MetaTable, pk=table_id)
        org = table.organization
        schema_name = f'org_{org.org_id}'
        column_name = column.name

        with connection.schema_editor() as schema_editor:
            model = self.create_dynamic_model(table, schema_name)
            field = model._meta.get_field(column_name)
            schema_editor.remove_field(model, field)

        column.delete()
        return Response(status=204)