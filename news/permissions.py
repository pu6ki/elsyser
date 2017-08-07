from rest_framework import permissions


class IsCommentAuthor(permissions.BasePermission):
    message = 'You must be the author of the comment in order to modify it.'

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
