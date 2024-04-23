#!/usr/bin/env python3
"""Contains Address model"""
from sync.models.user import BaseModel, models, MainUser


class IPAddress(models.Model):
    address = models.CharField(max_length=45, unique=True)
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.address
    
    class Meta:
        db_table = 'ip_addresses'