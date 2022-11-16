from operator import mod
import os
import sys
from django.conf import settings
from django.db import models
from django.dispatch import receiver

class Board(models.Model):
    title = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=10, null=False)
    content = models.TextField(null=False)
    password = models.CharField(max_length=20,null=False,default='1234')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    files = models.FileField(upload_to="",null=True)
    status = models.IntegerField(default=0,null=False)

    def __str__(self):
        return str(self.title)
    
@receiver(models.signals.pre_save, sender=Board)
def auto_delete_file_on_save(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False
    
    for field in instance._meta.fields:
        field_type = field.get_internal_type()
        if field_type == 'FileField' or field_type == 'ImageField':
            origin_file = getattr(old_obj, field.name)
            new_file = getattr(instance, field.name)
            print(origin_file, new_file)
            if origin_file != new_file and os.path.isfile(origin_file.path):
                os.remove(origin_file.path)

@receiver(models.signals.post_delete, sender=Board)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    for field in instance._meta.fields:
        field_type = field.get_internal_type()
        if field_type == 'FileField' or field_type == 'ImageField':
            origin_file = getattr(instance, field.name)
            if origin_file and os.path.isfile(origin_file.path):
                os.remove(origin_file.path)