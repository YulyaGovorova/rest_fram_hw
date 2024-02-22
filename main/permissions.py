from rest_framework import permissions
from rest_framework.permissions import BasePermission


class Moderator(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderator') and permissions.SAFE_METHODS:
            return True


class UserOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class UserPerm(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False