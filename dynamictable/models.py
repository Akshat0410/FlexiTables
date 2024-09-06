from django.db import models

class Organization(models.Model):
    org_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    db_type = models.CharField(max_length=10, choices=[('SQL', 'SQL'), ('NOSQL', 'NoSQL')])

class MetaTable(models.Model):
    table_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tables')

class MetaColumn(models.Model):
    column_id = models.AutoField(primary_key=True)
    table = models.ForeignKey(MetaTable, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=50)