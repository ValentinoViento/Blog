from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify


class Comentarios(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='blogs')            #asocio al modelo de blog, para que si un posteo es eliminado, el/los comentarios también
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = CKEditor5Field('Coment', config_name ='coment', blank=True)
    fechaCreado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor} commented on {self.blog.titulo}"


class Blog(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    texto = models.CharField(max_length=1000,db_index=True,unique=True,blank=True)
    fechaCreado = models.DateTimeField(auto_now_add=True)
    comentarios = models.ForeignKey(Comentarios, on_delete=models.CASCADE,null=True, blank=True, related_name='comentarios')  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super(Blog, self).save(*args, **kwargs) 
    

    def __str__(self):
        return self.titulo
    
