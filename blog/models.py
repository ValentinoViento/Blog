from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    titulo = models.TextField()
    texto = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.autor,self.texto