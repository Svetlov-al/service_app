from django.db.models import F, Prefetch, Sum
from django.core.cache import cache
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from service.settings import PRICE_CACHE_KEY
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

        price_cache = cache.get(PRICE_CACHE_KEY)

        if price_cache:
            total_amount = price_cache
        else:
            total_amount = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(PRICE_CACHE_KEY, total_amount, 60*60)
        respone_data = {'result': respone.data,
                        'total_price': total_amount}
        respone.data = respone_data

        return respone
