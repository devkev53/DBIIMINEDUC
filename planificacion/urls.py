from django.urls import path
from .views import PlanificacionView, PlanificacionCreateView, ActividadCreateView, ActividadDelete, PagoActividadCreateView

urlpatterns = [
	path('planificacion/', PlanificacionView.as_view(), name='planificacion'),
	path('planificacion/create', PlanificacionCreateView.as_view(), name='add_planificacion'),
	path('actividad/create', ActividadCreateView.as_view(), name='add_actividad'),
	path('actividad/pago', PagoActividadCreateView.as_view(), name='add_pago'),
	path('actividad/delete/<int:pk>', ActividadDelete.as_view(), name='delete_actividad'),
]