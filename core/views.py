from django.shortcuts import render
from django.utils import timezone

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, \
PermissionRequiredMixin

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .models import Departamento, Municipio
from escuela.models import Escuela

# Create your views here.

class Home(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "core/home.html"

class HomeSinPrivilegios(TemplateView):
    template_name = "core/sin_privilegios.html"

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'login'
    raise_exception=False
    redirect_field_name="redirect_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class DepartamentoListView(ListView):
    model = Departamento
    template_name = "core/prueba.html"

    def get_context_data(self, **kwargs):
        municipio = Municipio.objects.all()
        escuela = Escuela.objects.all()
        departamento = Departamento.objects.all()
        return {
        	'departamento': departamento, 'municipio': municipio,
        	'escuela': escuela
        	}