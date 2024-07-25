from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_instructor
