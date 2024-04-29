#!/usr/bin/env python3


"""Contains Document related views"""


from sync.serializers.document import DocumentSerializer, Document
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CreateDocumentView(views.APIView):
    """
    View for creating a document
    """
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """Handles creation of docs"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            Document.custom_save(**serializer.validated_data, owner=user)
            return Response({
                "message": 'Document Successfuly created!',
                "status": status.HTTP_201_CREATED
            })
        else:
            return Response({
                "error": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            })
    