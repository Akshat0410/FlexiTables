from django.http import JsonResponse
from .models import Organization, MetaTable, MetaColumn

def organization_models(request, org_id):
    try:
        # Retrieve the organization by its primary key (org_id)
        org = Organization.objects.get(pk=org_id)
        
        # Get all MetaTable objects associated with the organization
        tables = MetaTable.objects.filter(organization=org)
        
        # Prepare the response data structure
        response_data = {
            'organization': org.name,
            'tables': []
        }
        
        # Iterate over each table to get its columns
        for table in tables:
            # Get all MetaColumn objects associated with the table
            columns = MetaColumn.objects.filter(table=table)
            
            # Append table and its columns to the response data
            response_data['tables'].append({
                'table_name': table.name,
                'columns': [{'name': column.name, 'data_type': column.data_type} for column in columns]
            })
        
        # Return the response data as JSON
        return JsonResponse(response_data)
    
    except Organization.DoesNotExist:
        # Return an error response if the organization does not exist
        return JsonResponse({'error': 'Organization not found'}, status=404)