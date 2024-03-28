#!/usr/bin/env python3

"""Permission model for the Editor app"""

from sync.models.document import Document, User, BaseModel, models


class Permission(BaseModel):
    """
    Permission model
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions')
    can_edit = models.BooleanField(default=False)
    can_comment = models.BooleanField(default=False)

    class Meta:
        db_table = 'permissions'

    def __str__(self):
        return f'{self.document.title} - {self.user.email}'
