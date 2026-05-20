from django.db import models

from django.contrib.auth.models import User

class Todo(models.Model):
    doer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    todo_note = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField('date published')
