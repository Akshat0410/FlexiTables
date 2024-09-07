from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import MetaTable, MetaColumn
from .helpers import get_dynamic_model
from rest_framework import serializers

class DynamicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # This will be set dynamically
        fields = '__all__'

class DataIngestionViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return MetaTable.objects.none() 
    
    def get_serializer_class(self):
        model = get_dynamic_model(self.kwargs['org_id'], self.kwargs['table_id'])
        DynamicModelSerializer.Meta.model = model
        return DynamicModelSerializer
    
    def create(self, request, org_id, table_id):
        data = request.data
        operation = data['data']['operation']
        model = get_dynamic_model(org_id, table_id)
        if operation == 'add':
            for row in data['data']['rows']:
                if 'id' not in row:
                    return Response({"error": "ID is mandatory"}, status=status.HTTP_400_BAD_REQUEST)
                model.objects.create(**row)
            return Response({"message": "Data inserted successfully"}, status=status.HTTP_201_CREATED)
        elif operation == 'update':
            for row in data['data']['rows']:
                obj = get_object_or_404(model, id=row['id'])
                update_fields = []
                for key, value in row.items():
                    if key != 'id':
                        setattr(obj, key, value)
                        update_fields.append(key)
                obj.save(update_fields=update_fields)
            return Response({"message": "Data updated successfully"}, status=status.HTTP_200_OK)
        elif operation == 'delete':
            for row in data['data']['rows']:
                obj = get_object_or_404(model, id=row['id'])
                obj.delete()
            return Response({"message": "Data deleted successfully"}, status=status.HTTP_200_OK)