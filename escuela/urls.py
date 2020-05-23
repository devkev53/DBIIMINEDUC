from django.urls import path

from .views import EscuelaListView, EscuelaCreate, load_municipios, EscuelaDelete, EscuelaUpdate

urlpatterns = [
	path('list/', EscuelaListView.as_view(), name='list_escuela'),
	path('registrar', EscuelaCreate.as_view(), name='create_escuela'),
	path('eliminar/<slug:pk>', EscuelaDelete.as_view(), name='eliminar_escuela'),
	path('actualizar/<slug:pk>', EscuelaUpdate.as_view(), name='actualizar_escuela'),
	# Url para cargar el template municipios con ajax
	path('ajax/load_muni/', load_municipios, name='ajax_load_muni'),
]
