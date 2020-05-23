'''
    from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound

from django.core import serializers
from django.http import JsonResponse
import json

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from perfil.models import UsuarioEscuela
from escuela.models import Escuela, Comite
from planificacion.models import Planificacion
from padre.models import PadreFamilia
from perfil.models import UsuarioComite

from .forms import IntegranteForm
from .models import Integrante, Fondo, MovimientoFondo

from easy_pdf.views import PDFTemplateView

from core.views import SinPrivilegios
'''

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import Http404

from django.core import serializers
from django.http import JsonResponse
import json

from core.views import SinPrivilegios

from django.core.exceptions import SuspiciousOperation
from django.contrib import messages

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from .models import Planificacion, Actividad, PagoActividad
from escuela.models import Comite
from perfil.models import UsuarioComite

from .forms import PagoActividadForm

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

# Formularios en linea
from django.forms import inlineformset_factory

# Create your views here.

class PlanificacionView(SinPrivilegios, TemplateView):
    permission_required = ['escuela.view_comite']
    login_url = 'login'
    template_name = "planificacion/planificacion_list.html"
    context = []

    def get_context_data(self, **kwargs):
        context = super(PlanificacionView, self).get_context_data(**kwargs)
        context.update(**kwargs)
        # Iniciamos a enviar los contextos

        # Obtenemos el usuario
        usuario = self.request.user

        # Obtenemos el Perfil
        perfil = UsuarioComite.objects.filter(usuario=usuario).get()
        # Obtenemos el Comite
        comite = None
        for c in Comite.objects.all():
        	if perfil.comite == c:
        		comite = c
        context['comite'] = comite
        # Obtenemos las Planificaciones
        planificaciones = Planificacion.objects.filter(comite=comite)
        context['planificaciones'] = planificaciones
        # Traemos todas las actividades
        context['actividades'] = Actividad.objects.all()
        return context

class PlanificacionCreateView(SinPrivilegios, CreateView):
    permission_required = ['planificacion.add_planificacion',]
    model = Planificacion
    fields = '__all__'
    success_url = reverse_lazy('planificacion')

    def form_invalid(self, form):
        messages.error(request, "Error")

class ActividadCreateView(SinPrivilegios, CreateView):
    permission_required = ['planificacion.add_actividad',]
    model = Actividad
    fields = '__all__'
    success_url = reverse_lazy('planificacion')

    def form_invalid(self, form):
        messages.error(request, "Error")

class ActividadDelete(SinPrivilegios, DeleteView):
    permission_required = ['planificacion.delete_actividad']
    model = Actividad
    success_url = reverse_lazy('planificacion')

class PagoActividadCreateView(SinPrivilegios, CreateView):
    permission_required = ['planificacion.add_pagoactividad',]
    model = PagoActividad
    form_class = PagoActividadForm
    success_url = reverse_lazy('planificacion')

    def form_invalid(self, form):
        messages.error(request, "Error")