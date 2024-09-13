from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class RegistroUsuario(CreateView):
    template_name = 'registration/registro.html'   #por defecto se deja en template y se llama de manera normal, por separarlo y unificar el login/registro, lo modifico a la ruta "/registration" y lo llamo la ruta de esta manera
    form_class = UserCreationForm
    success_url = reverse_lazy('login')




class CrearPost(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['autor','título', 'texto']
    template_name = 'crear_post.html'
    success_url = reverse_lazy('tus_posts')

    def form_valid(self, form):
        form.instance.remitente = self.request.user
        return super().form_valid(form)


class VerBlog(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'ver_blog.html'

    def get_queryset(self):
        return Blog.objects.all()


class MisPosts(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'tus_posts.html'

    def get_queryset(self):
        return Blog.objects.filter(autor=self.request.user)
    
    
class EliminarPosts(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('tus_posts')

    def get_object(self, queryset=None):
        return get_object_or_404(Blog, pk=self.kwargs['pk'], autor=self.request.user) #si encuentra el objeto, consigue su "pk" para decidir eliminarlo



def home_view(request):
    return render(request, 'home.html')