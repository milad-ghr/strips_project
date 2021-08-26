from rest_framework.permissions import BasePermission

NORMAL_USER_VIEW_METHODS_PERMISSIONS = ['GET', 'PUT', 'PATCH', 'DELETE']


class UsersPermissionClass(BasePermission):
    """
    This class has two main function, `has_permission` for grant accessing specific view or action and
        `has_object_permission` to grant permission on specific object.
    """

    def has_permission(self, request, view):
        """
        All Users has the permission to view their account info, so all user has permission.
        """
        if request.user.is_staff is True or request.user.is_superuser is True or \
                request.method in NORMAL_USER_VIEW_METHODS_PERMISSIONS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Admins can edit users information and all requires actions, but a normal user can only see it's information.
        """
        if request.user.is_staff is True or request.user.is_superuser is True or request.user.id == obj.id:
            return True
        return False
