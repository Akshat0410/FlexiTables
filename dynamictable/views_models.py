from django.http import JsonResponse
from .models import Organization, MetaTable, MetaColumn

def organization_models(request, org_id):
    try:
        org = Organization.objects.get(pk=org_id)
        tables = MetaTable.objects.filter(organization=org)
        response_data = {
            'organization': org.name,
            'tables': []
        }
        for table in tables:
            columns = MetaColumn.objects.filter(table=table)
            response_data['tables'].append({
                'table_name': table.name,
                'columns': [{'name': column.name, 'data_type': column.data_type} for column in columns]
            })
        return JsonResponse(response_data)
    except Organization.DoesNotExist:
        return JsonResponse({'error': 'Organization not found'}, status=404)