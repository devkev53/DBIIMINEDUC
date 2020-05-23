from django.urls import path

from .views import EscuelaUsuarioCreate, UsuarioComiteCreate

urlpatterns = [
	path('registrarUsuarioEscuela/', EscuelaUsuarioCreate.as_view(), name='create_escuela_usuario'),
	path('registrarUsuarioComite/', UsuarioComiteCreate.as_view(), name='create_comite_usuario'),
]
