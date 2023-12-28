from django.db.models import F, Prefetch, Sum
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    price_with_discount = (
            F('service__full_price') -
            F('service__full_price') *
            F('plan__discount_percent') / 100.00
    )
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client',
                 queryset=Client.objects.all().select_related(
                     'user',
                 ).only('company_name',
                        'user__email')
                 )
    ).annotate(
        price=price_with_discount
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        respone = super().list(request, *args, **kwargs)

        respone_data = {'result': respone.data,
                        'total_amount': queryset.aggregate(total=Sum('price')).get('total')}
        respone.data = respone_data

        return respone
