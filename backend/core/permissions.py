from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners to access their objects.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPublicReadable(permissions.BasePermission):
    """
    Custom permission for objects with privacy settings.
    """
    
    def has_object_permission(self, request, view, obj):
        # Owner always has access
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        
        # Check privacy level
        if hasattr(obj, 'privacy_level'):
            if obj.privacy_level == 'public':
                return True
            elif obj.privacy_level == 'friends' and request.user.is_authenticated:
                # Check if users are friends (if implemented)
                return True
        
        return False