import django_filters
from django_filters.rest_framework import filters


class CreatedAtFilterSet(django_filters.FilterSet):
    date_from = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="created_at", lookup_expr="lte")
