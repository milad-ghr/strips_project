from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer


class ProductsAPIView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def filter_queryset(self, queryset):
        return queryset.filter(active=True)

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('id'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
