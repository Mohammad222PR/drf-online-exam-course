from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_instructor


class IsInstructorOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.instructor_id


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_student
