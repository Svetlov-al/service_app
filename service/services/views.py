from django.db.models import F, Prefetch, Sum
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = (Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client',
                 queryset=Client.objects.all().select_related(
                     'user',
                 ).only('company_name',
                        'user__email')
                 ))
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        respone = super().list(request, *args, **kwargs)

        respone_data = {'result': respone.data,
                        'total_amount': queryset.aggregate(total=Sum('price')).get('total')}
        respone.data = respone_data

        return respone
