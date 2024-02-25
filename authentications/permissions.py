from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access a view.
    """
    message = "Only admin users can access this endpoint."
    def has_permission(self, request, view):
        is_admin = bool(request.user and request.user.role.name == 'admin')
        if not is_admin:
            self.message = 'Only an admin can perform this task.'
        return is_admin


    
class IsCreatorUser(permissions.BasePermission):
    """
    Custom permission to only allow creator users to access a view.
    """
    message = "Only creator users can access this endpoint."
    def has_permission(self, request, view):
        is_creator = bool(request.user and request.user.role.name == 'creator')
        if not is_creator:
            self.message = 'Only a creator can perform this task.'
        return is_creator
    
class IsViewerUser(permissions.BasePermission):
    """
    Custom permission to only allow viewer users to access a view.
    """
    message = "Only viewer users can access this endpoint."
    def has_permission(self, request, view):
        is_viewer = bool(request.user and request.user.role.name == 'viewer')
        if not is_viewer:
            self.message = 'Only a viewer can perform this task.'
        return is_viewer
    
class IsVerifierUser(permissions.BasePermission):
    """
    Custom permission to only allow verifier users to access a view.
    """
    message = "Only verifier users can access this endpoint."
    def has_permission(self, request, view):
        is_verifier = bool(request.user and request.user.role.name == 'verifier')
        if not is_verifier:
            self.message = 'Only a verifier can perform this task.'
        return is_verifier
    
class IsApproverUser(permissions.BasePermission):
    """
    Custom permission to only allow approver users to access a view.
    """
    message = "Only approver users can access this endpoint."
    def has_permission(self, request, view):
        is_approver = bool(request.user and request.user.role.name == 'approver')
        if not is_approver:
            self.message = 'Only an approver can perform this task.'
        return is_approver
    
class IsHeaderUser(permissions.BasePermission):
    """
    Custom permission to only allow header users to access a view.
    """
    message = "Only header users can access this endpoint."
    def has_permission(self, request, view):
        is_header = bool(request.user and request.user.role.name == 'header')
        if not is_header:
            self.message = 'Only a header can perform this task.'
        return is_header


class IsMinisterUser(permissions.BasePermission):
    """
    Custom permission to only allow minister users to access a view.
    """
    message = "Only minister users can access this endpoint."
    def has_permission(self, request, view):
        is_minister = bool(request.user and request.user.role.name == 'minister')
        if not is_minister:
            self.message = 'Only a minister can perform this task.'
        return is_minister
    

