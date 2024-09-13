from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class RegistroUsuario(CreateView):
    template_name = 'registration/registro.html'   #por defecto se deja en template y se llama de manera normal, por separarlo lo modifico a registration y le cambio la ruta de esta manera
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    



class CrearPost(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['autor', 'texto']
    template_name = 'crear_post.html'
    success_url = reverse_lazy('ver_post')
    
    def form_valid(self, form):
        form.instance.remitente = self.request.user
        return super().form_valid(form)
    
    
# class MensajesRecibidos(LoginRequiredMixin, ListView):
#     model = Mensaje
#     template_name = 'mensajes_recibidos.html'
    
#     def get_queryset(self):
#         return Mensaje.objects.filter(destinatario=self.request.user)
    
    
# class EliminarMensaje(LoginRequiredMixin, DeleteView):
#     model = Mensaje
#     template_name = 'confirmar_eliminacion.html'
#     success_url = reverse_lazy('mensajes_recibidos')
    
#     def get_queryset(self):
#         return Mensaje.objects.filter(destinatario=self.request.user)
        
    
def home_view(request):
    return render(request, 'home.html')