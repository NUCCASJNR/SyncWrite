#!/usr/bin/env python3

"""Comment model for the Editor app"""

from sync.models.document import Document, User, BaseModel, models


class Comment(BaseModel):
    """
    Comment model
    """
    content = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return self.content
