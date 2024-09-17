from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField # type: ignore


class Blog(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    texto = RichTextField()

    def __str__(self):
        return self.titulo