#!/usr/bin/env python3

"""Base model"""

from django.db import models
from typing import Any, Dict
from cloudinary.models import CloudinaryResource
from django.utils import timezone
from uuid import uuid4
from django.contrib.auth.hashers import make_password


class BaseModel(models.Model):
    """Base model for CrowdFunding
    Every other class inherits from this class
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

    @classmethod
    def custom_save(cls, **kwargs: Dict[str, Any]):
        """
        Saves an instance of the class
        """
        # cls.updated_at = datetime.now()
        instance = cls.objects.create(**kwargs)
        return instance

    @classmethod
    def custom_get(cls, **kwargs):
        try:
            instance = cls.objects.get(**kwargs)
            return instance
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_all(cls):
        """Get all objs of a cls"""
        return cls.objects.all()

    @classmethod
    def custom_delete(cls, **kwargs: Dict[str, Any]):
        """
        Deletes an instance of the class Based
        on the kwargs filter
        """
        instance = cls.objects.filter(**kwargs)
        instance.delete()

    @classmethod
    def custom_update(cls, filter_kwargs: Dict[str, Any], update_kwargs: Dict[str, Any]):
        """
        Updates instances of the class based on the filter_kwargs and update_kwargs.
        """
        try:
            if 'password' in update_kwargs and update_kwargs['password'] is not None:
                update_kwargs['password'] = make_password(update_kwargs['password'])

            cls.objects.filter(**filter_kwargs).update(**update_kwargs)
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def find_objs_by(cls, **kwargs: Dict[str, Any]):
        """
        Finds an instance of the class Based
        on the kwargs
        """
        try:
            instance = cls.objects.filter(**kwargs)
            return instance
        except cls.DoesNotExist:
            return "No instances found"

    @classmethod
    def find_obj_by(cls, **kwargs: Dict[str, Any]):
        """
        Finds an instance of the class Based
        on the kwargs
        """
        try:
            instance = cls.objects.filter(**kwargs).first()
            return instance
        except cls.DoesNotExist:
            return "No such instance"

    @classmethod
    def filter_count(cls, **kwargs: Dict[str, Any]):
        """
        Counts the number of instances of the class
        """
        return cls.objects.filter(**kwargs).count()

    @classmethod
    def count(cls):
        """
        Counts the number of instances of the class
        """
        return cls.objects.count()
    
    @classmethod
    def filter_objects(cls, **kwargs: Dict[str, Any]):
        """
        Retrieves queryset of instances of the class based on provided filter criteria
        """
        return cls.objects.filter(**kwargs)
    
    @classmethod
    def handle_cloudinary_resource(cls, cloudinary_resource: CloudinaryResource) -> Dict[str, Any]:
        """
        Converts a CloudinaryResource object to a dictionary
        """
        if isinstance(cloudinary_resource, CloudinaryResource):
            return {
                'url': cloudinary_resource.public_id
            }
        else:
            return {}

    @classmethod
    def to_dict(cls, obj: Any) -> Dict[str, Any]:
        """
        Converts the object to a dictionary
        @type obj: object
        """

        model_dict = {}
        for field in obj._meta.fields:
            field_name = field.name
            field_value = getattr(obj, field_name)
            if isinstance(field, models.DateTimeField):
                field_value = field_value.isoformat() if field_value else None
            elif isinstance(field, models.UUIDField):
                field_value = str(field_value)
            elif isinstance(field, models.ImageField):
                field_value = field_value.url if field_value else None
            elif isinstance(field, CloudinaryResource):
                # Here, handle the conversion for CloudinaryResource
                field_value = cls.handle_cloudinary_resource(field_value)
            model_dict[field_name] = field_value

        return model_dict


    
