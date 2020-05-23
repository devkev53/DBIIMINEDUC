from django.urls import path
from .views import ComiteEscuela, IntegranteCreate, SearchPadre, IntegranteDelete, \
MovimientoCreateView, HelloPDFView, ComiteUsuario

urlpatterns = [
	path('usuario/', ComiteUsuario.as_view(), name='comite_usuario'),
	path('escuela/', ComiteEscuela.as_view(), name='comite'),
	path('registrar/integrante/', IntegranteCreate.as_view(), name='crear_intengrante'),
	path('search/padre/', SearchPadre, name='padre_ajax'),
	path('eliminar/integrante/<int:pk>', IntegranteDelete.as_view(), name='eliminar_intengrante'),
	path('asignarFondo/', MovimientoCreateView.as_view(), name='asignar'),
	path('registro/movimientos', HelloPDFView.as_view(), name='pdf_movimientos'),
]
