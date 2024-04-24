#!/usr/bin/env python3
"""Contains Address model"""
from sync.models.user import BaseModel, models, MainUser


class IPAddress(BaseModel):
    address = models.CharField(max_length=45)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='authorized_ips')

    def __str__(self):
        return self.address
    
    class Meta:
        db_table = 'ip_addresses'
        unique_together = ['address', 'user']