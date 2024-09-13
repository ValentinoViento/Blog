from django.urls import path
from pages import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('enviar/', views.CrearMensaje.as_view(), name='enviar_mensaje'),
    path('recibidos/', views.MensajesRecibidos.as_view(), name='mensajes_recibidos'),
    path('eliminar/<int:pk>', views.EliminarMensaje.as_view(), name='eliminar_mensaje'),
]
