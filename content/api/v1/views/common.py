from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from _core.permission import ListPermission, CreatePermission, RetrievePermission, UpdatePermission, DeletePermission


class BaseListCreateView(ListCreateAPIView):
    def get_permissions(self):
        return [ListPermission() if self.request.method == "GET" else CreatePermission()]


class BaseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        match self.request.method:
            case "GET":
                return [RetrievePermission()]
            case "PUT":
                return [UpdatePermission()]
            case "PATCH":
                return [UpdatePermission()]
            case "DELETE":
                return [DeletePermission()]
