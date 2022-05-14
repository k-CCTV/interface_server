from django.conf import settings
from django.db import models
import sys, os

class Board(models.Model):
    author = models.CharField(max_length=10, null=False)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(null= False, upload_to = "images/")
    fileType = models.CharField(max_length=10, null= True)

    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        mod = getattr(sys.modules[__name__], self._meta.object_name)

        try:
            obj = mod.objects.get(id=self.id)
        except:
            obj = None
            super(mod, self ).save(*args, **kwargs)
            return
        else:
            for field in obj._meta.fields:
                field_type = field.get_internal_type()
        if field_type == 'FileField' or field_type == 'ImageField':
            origin_file = getattr(obj, field.name)
            new_file = getattr(self, field.name)
            if origin_file != new_file:
                path = '.' + origin_file.url
                if os.path.isfile(path):
                    os.remove(path)
        super(mod, self).save(*args, **kwargs)
        return
    
    def delete(self, *args, **kargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(Board,self).delete(*args,**kargs)