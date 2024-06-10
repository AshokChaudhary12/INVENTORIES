# import django_filters
# from django.db.models import Q
# from my_app.models import Inventories
#
#
# class InventoriesFilters(django_filters.FilterSet):
#     q = django_filters.CharFilter(method='my_custom_filter', label="Search")
#     purchase_date = django_filters.DateFilter(field_name='purchase_date', lookup_expr='exact', label='Purchase Date')
#     purchase_date__gt = django_filters.DateFilter(field_name='purchase_date', lookup_expr='gt', label='Purchased After')
#     purchase_date__lt = django_filters.DateFilter(field_name='purchase_date', lookup_expr='lt',
#                                                   label='Purchased Before')
#     purchase_date_range = django_filters.DateFromToRangeFilter(field_name='purchase_date', label='Purchase Date Range')
#
#     class Meta:
#         model = Inventories
#         fields = ['name', 'inventry_type', 'purchase_date']
#
#     def my_custom_filter(self, queryset, name, value):
#         return queryset.filter(
#             Q(name__icontains=value) |
#             Q(inventry_type__name__icontains=value)
#         )
