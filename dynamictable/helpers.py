from django.apps import apps
from .models import MetaTable, MetaColumn
from django.db import models
from typing import List

FIELD_TYPE_MAPPING = {
    'IntegerField': models.IntegerField,
    'BooleanField': models.BooleanField,
    'CharField': models.CharField,
}

def get_dynamic_model(org_id, table_id):
    meta_table: MetaTable = MetaTable.objects.get(table_id=table_id, organization_id=org_id)
    schema_name = f"org_{org_id}"
    table_name = meta_table.name
    
    # Retrieve columns from MetaColumn table
    meta_columns: List[MetaColumn] = MetaColumn.objects.filter(table_id=table_id)
    
    # Create a dictionary of field names and their types
    fields = {}
    for column in meta_columns:
        field_class = FIELD_TYPE_MAPPING.get(column.data_type)
        if field_class:
            # Add the field to the fields dictionary
            if field_class == models.CharField:
                fields[column.name] = field_class(max_length=255)  # Adjust max_length as needed
            else:
                fields[column.name] = field_class()
    
    DynamicModel = type(table_name, (models.Model,), {
            '__module__': 'dynamictable.models',
            'Meta': type('Meta', (), {
                'db_table': f'"{schema_name}"."{table_name}"'  # Ensure schema and table name are quoted
            }),
            **fields
        })
    return apps.get_model('dynamictable', DynamicModel.__name__.lower())