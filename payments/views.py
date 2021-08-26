from rest_framework import generics

from .models import Payment
from .serializers import PaymentSerializer, CardSerializer


class PaymentAPIView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def filter_queryset(self, queryset):
        if not self.request.user.is_staff:
            queryset = queryset.filter(strip_customer__user__id=self.request.user.id)
        return queryset

    def get(self, request, *args, **kwargs):
        if kwargs.get('id'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class AddCardAPIView(generics.CreateAPIView):
    serializer_class = CardSerializer()
