import django_filters
from .models import DebitTransaction

class DebitTransactionFilter(django_filters.FilterSet):
    class Meta:
        model = DebitTransaction
        fields = ['balanced']
