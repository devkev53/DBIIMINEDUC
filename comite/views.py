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

# Create your views here.

'''     -       VISTAS PRINCIPALES DEL COMITE       -    '''
class ComiteEscuela(SinPrivilegios, TemplateView):
    permission_required = ['escuela.view_comite']
    login_url = 'login'
    template_name = "comite/comite.html"
    context = []

    def get_context_data(self, **kwargs):
        context = super(ComiteEscuela, self).get_context_data(**kwargs)
        context.update(**kwargs)
        # usuario =  UsuarioEscuela.objects.filter(usuario=)
        usuario = self.request.user

        context['perfil'] = UsuarioEscuela.objects.filter(usuario=usuario).get()
        context['comite'] = Comite.objects.all()
        user = UsuarioEscuela.objects.filter(usuario=usuario).get()
        comiteEscuela = Comite.objects.filter(escuela=user.escuela).get()
        user_comite = UsuarioComite.objects.filter(comite=comiteEscuela)
        context['usuario'] = user_comite
        fondo_comite = Fondo.objects.filter(comite=comiteEscuela).first()
        comite_fondo = fondo_comite

        movimientos_fondo = MovimientoFondo.objects.filter(fondo=comite_fondo)
        # context['fondo'] = Fondo.objects.filter(comite=comiteEscuela).first()
        context['fondo'] = Fondo.objects.filter(comite=comiteEscuela).first()
        context['movimientos'] = movimientos_fondo
        # context['movimientos'] = MovimientoFondo.objects.filter(fondo=fondo_comite)
        context['integrantes'] = Integrante.objects.filter(comite=comiteEscuela)
        context['planificacion'] = Planificacion.objects.filter(comite=comiteEscuela)
        return context

# Crear un itengrante desde el usuario del COMITE
class IntegranteCreate(SinPrivilegios, CreateView):
    permission_required = ['comite.add_integrante', 'padre.add_padrefamilia']
    model = Integrante
    form_class = IntegranteForm
    success_url = reverse_lazy('comite')

    def form_valid(self, form):
        persona = form['persona'].save()
        integrante = form['integrante'].save(commit=False)
        integrante.padre = persona
        integrante.save()
        return HttpResponseRedirect(reverse_lazy('comite'))

    def form_invalid(self, form):
        return HttpResponseNotFound('<h1>Page not found</h1>')

def SearchPadre(request):
    # Obtenemos el dato que envia el formulario
    dpi = request.GET.get('dpi')

    if PadreFamilia.objects.filter(dpi=dpi):
        padre = PadreFamilia.objects.filter(dpi=dpi).values()
        return JsonResponse({"Padre": list(padre)})
    else:
        return JsonResponse({"error": True, "error": "there was an error"})

# Eliminar un itengrante desde el usuario del COMITE
class IntegranteDelete(SinPrivilegios, DeleteView):
    permission_required = ['comite.delete_integrante', 'padre.delete_padrefamilia']
    model = Integrante
    success_url = reverse_lazy('comite')

class AddFondoCreateView(SinPrivilegios, CreateView):
    permission_required = ['comite.delete_integrante', 'padre.delete_padrefamilia']
    model = Fondo

class MovimientoCreateView(SinPrivilegios, CreateView):
    permission_required = ['comite.add_movimientofondo',]
    model = MovimientoFondo
    fields = '__all__'
    success_url = reverse_lazy('comite')

    def form_invalid(self, form):
        messages.error(request, "Error")


# Vista del comite para el usuario del COMITE
class ComiteUsuario(SinPrivilegios, TemplateView):
    permission_required = ['escuela.view_comite']
    login_url = 'login'
    template_name = "comite/comite_usuario.html"
    context = []

    def get_context_data(self, **kwargs):
        context = super(ComiteUsuario, self).get_context_data(**kwargs)
        context.update(**kwargs)
        # usuario =  UsuarioComite.objects.filter(usuario=)
        usuario = self.request.user

        # Obtenemos el perfil para obtener el comite
        perfil = UsuarioComite.objects.filter(usuario=usuario).get()
        context['perfil'] = perfil
        escuela = Escuela.objects.all()
        ''' Con esta consulta buscamos arriba de comite y
        verificamos que el usuario pertenezca al comite de la escuela '''
        comite_escuela = Comite.objects.select_related('escuela').filter(escuela=perfil.comite.escuela).get()
        context['comite'] = comite_escuela
        # Obtenemos el Fondo
        fondo = Fondo.objects.filter(comite=comite_escuela).first()
        context['fondo'] = Fondo.objects.filter(comite=comite_escuela).first()
        # Envimos los integrantes
        context['integrantes'] = Integrante.objects.filter(comite=comite_escuela)
        # Enviamos los movimientos
        context['movimientos'] = MovimientoFondo.objects.filter(fondo=fondo).exists()
        return context

'''     -       VISTAS DE REPORTE PARA EL COMITE       -    '''

class  HelloPDFView( PDFTemplateView ):
    template_name  =  'comite/Reportes/registro_movimientos.html'
