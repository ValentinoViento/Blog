from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog, Comentarios
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.messages import success
from django_ckeditor_5.widgets import CKEditor5Widget



class RegistroUsuario(CreateView):
    template_name = 'registration/registro.html'   #por defecto se deja en template y se llama de manera normal, por separarlo y unificar el login/registro, lo modifico a la ruta "/registration" y lo llamo la ruta de esta manera
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


#creación de posts
class BlogForm(forms.ModelForm):
    class Meta:
          model = Blog
          fields = ("titulo", "texto")
          widgets = {
              "texto": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="texto"
              )
          }
        
class CrearPost(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'crear_post.html'
    success_url = reverse_lazy('mis_posts')

    def form_valid(self, form):
        form.instance.autor = self.request.user  # asigna el usuario actual como autor
        return super().form_valid(form)
    



#blog,contenido y comentarios
class VerBlog(ListView):
    model = Blog
    template_name = 'ver_blog.html'
    paginate_by = 4                     #sólo 4 posts por página

    def get_queryset(self):
        return Blog.objects.all().order_by('-fechaCreado')            #para ver a todos los usuarios y sus posts en orden por fecha


class BlogContenido(DetailView):
    model = Blog
    template_name = 'blog_contenido.html'         

    def get_context_data(self, **kwargs):                           #método heredado de la clase View, para renderizar y procesar vistas
        context = super().get_context_data(**kwargs)            #context = diccionario | **kwargs = argumentos claves

        if self.object:             
            context['comentarios'] = self.object.comentarios.all()          #si existe, se basa en la clave 'comentarios'
            context['form'] = ComentarioForm()                              #se crea con el formulario de más abajo
        context['blog_content'] = self.object.texto             #agrega el context al post
        return context
    
    def post(self, request):
        self.object = self.get_object()                 #recibe y almacena el objeto pedido
        form = ComentarioForm(request.POST)
        if form.is_valid():                             #comprobación del formulario válido, agregado tras algún error pasado
            comentario = form.save(commit=False)
            comentario.blog = self.object
            comentario.autor = request.user
            comentario.save()
            return redirect('blog_contenido', slug=self.object.slug)                  
        return self.render_to_response(self.get_context_data(form=form))


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentarios
        fields = ['texto']
        widgets = {
            'blog': forms.HiddenInput(),                #se esconde el "blog" de comentarios, para no mostrarse a la hora de crear un comentario
        }                                               #solía salir cómo opción a elegir el post a comentar, y era innecesario ya que el comentario tenía la "id" del post

    




#ver tus propios posts y tener la posibilidad de eliminarlos
class MisPosts(LoginRequiredMixin, View):
    template_name = 'mis_posts.html'

    def get(self, request):
        posts = Blog.objects.filter(autor=request.user)
        return render(request, self.template_name, {'object_list': posts})

    def post(self, request):
        seleccion = request.POST.getlist('seleccion')
        if request.POST.get("confirmar_eliminacion"):
            # Eliminar los posts seleccionados
            Blog.objects.filter(pk__in=seleccion, autor=request.user).delete()
            success(request, 'Posts eliminados exitosamente.')  # Add success message
            return redirect('mis_posts')
        else:
            # Mostrar la página de confirmación
            posts_seleccion = Blog.objects.filter(pk__in=seleccion, autor=request.user)
            return render(request, 'confirmar_eliminacion.html', {'posts_seleccion': posts_seleccion})




#vista home
def home_view(request):
    return render(request, 'home.html')