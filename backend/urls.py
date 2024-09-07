"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dynamictable.views import OrganizationViewSet, TableViewSet, ColumnViewSet
from rest_framework.routers import DefaultRouter
from dynamictable.views_models import organization_models
from dynamictable.views_data import DataIngestionViewSet


router = DefaultRouter(trailing_slash=False)

router.register(r"organizations/?", OrganizationViewSet, basename="organizations")
router.register(r"organizations/(?P<org_id>[^/.]+)/tables/?", TableViewSet, basename="tables")
router.register(r"organizations/(?P<org_id>[^/.]+)/tables/(?P<table_id>[^/.]+)/columns/?", ColumnViewSet, basename="columns")
router.register(r"organizations/(?P<org_id>[^/.]+)/tables/(?P<table_id>[^/.]+)/data/?", DataIngestionViewSet, basename="data")

urlpatterns = [
    path('organizations/<int:org_id>/models/', organization_models, name='organization_models'),

    path('', include(router.urls)),
]
