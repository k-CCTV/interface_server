from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=10, null=False)
    content = models.TextField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    files = models.FileField(upload_to="",null=True)
    status = models.IntegerField(default=0,null=False)

    def __str__(self):
        return str(self.title)