from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from _core.permission import IsSuperUser

from account.api.v1.serializers import RoleSerializer, RolePermSerializer
from account.models import Role, RolePerm


class RoleListCreateView(ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsSuperUser,)


class RoleRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsSuperUser,)


class RolePermissionListUpdateView(GenericAPIView, ListModelMixin):
    queryset = RolePerm.objects.all()
    serializer_class = RolePermSerializer
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return self.queryset.filter(role=self.kwargs["pk"])

    def get_serializer(self, *args, **kwargs):
        kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    @extend_schema(
        responses={200: RolePermSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={204: None},
    )
    def patch(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        context["role"] = get_object_or_404(Role, pk=self.kwargs["pk"])
        serializer = self.get_serializer(data=request.data, many=True, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
