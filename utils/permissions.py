from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        req_user = request.user.username
        if obj.__class__ == User:
            return obj.username == req_user
        else:
            return obj.user == request.user
