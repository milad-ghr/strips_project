from rest_framework import generics, permissions

from .models import User, Subscription
from .serializers import UserSerializer, SubscriptionSerializer
from .permissions import UsersPermissionClass


class UserAPIView(generics.ListAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    permission_classes = [permissions.IsAuthenticated, UsersPermissionClass]

    def filter_queryset(self, queryset):
        if not self.request.user.is_staff:
            queryset = queryset.filter(id=self.request.user.id)
        return queryset

    def get(self, request, *args, **kwargs):
        if kwargs.get('id'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


# class SubscriptionAPIView(generics)