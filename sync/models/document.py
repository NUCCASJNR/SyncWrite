#!/usr/bin/env python3

"""Document model for the Editor app"""

from sync.models.user import BaseModel, MainUser as User, models


class Document(BaseModel):
    """
    Document model
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_documents')
    collaborators = models.ManyToManyField(User, related_name='collaborated_documents')
    
    class Meta:
        db_table = 'documents'

    def __str__(self):
        return self.title
