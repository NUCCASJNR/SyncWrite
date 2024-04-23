#!/usr/bin/env python3


"""Contains Document serializer"""

from rest_framework import serializers
from sync.models.document import Document


class DocumentSerializer(serializers.ModelSerializer):
    """
    Document serializer
    """
    owner_email = serializers.EmailField(source='owner.email')
    collaborator_emails = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ('title', 'content', 'owner_email', 'collaborator_emails')

    def get_collaborator_emails(self, obj):
        return [collaborator.email for collaborator in obj.collaborators.all()]
