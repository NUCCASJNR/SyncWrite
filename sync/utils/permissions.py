#!/usr/bin/env python3

"""
contains custom permissions for the sync app
"""

from rest_framework.permissions import BasePermission
from sync.models.permission import Document, Permission

class HasEditAccess(BasePermission):
    """
    Custom permission to only allow users to edit document
    """
    
    def has_permission(self, request, view):
        """
        Check if the requesting user has edit access for the document.
        """
        document_id = request.data.get('document_id')
        if not document_id:
            return False
        try:
            document = Document.custom_get(id=document_id)
        except Document.DoesNotExist:
            return False
        user = request.user
        try:
            permission = Permission.objects.get(document=document, user=user)
            return permission.can_edit
        except Permission.DoesNotExist:
            return False


class HasCommentAccess(BasePermission):
    """
    Custom permission to only allow users to comment on document
    """
    
    def has_permission(self, request, view):
        """
        Check if the requesting user has comment access for the document.
        """
        document_id = request.data.get('document_id')
        if not document_id:
            return False
        try:
            document = Document.custom_get(id=document_id)
        except Document.DoesNotExist:
            return False
        user = request.user
        try:
            permission = Permission.objects.get(document=document, user=user)
            return permission.can_comment
        except Permission.DoesNotExist:
            return False
