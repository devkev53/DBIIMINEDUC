from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound

from django.views.generic.edit import CreateView
from core.views import SinPrivilegios

from .forms import EscuelaUsuarioForm, ComiteUsuarioForm
from .models import UsuarioEscuela, UsuarioComite

# Create your views here.

class EscuelaUsuarioCreate(CreateView):
    model = UsuarioEscuela
    form_class = EscuelaUsuarioForm
    success_url = reverse_lazy('list_escuela')

    def form_valid(self, form):
    	auth_user = form['user'].save()
    	user_escuela = form['usuario'].save(commit=False)
    	user_escuela.usuario = auth_user
    	user_escuela.save()
    	return HttpResponseRedirect(reverse_lazy('list_escuela'))

    def form_invalid(self, form):
     	return HttpResponseNotFound('<h1>Page not found</h1>')

class UsuarioComiteCreate(SinPrivilegios, CreateView):
    permission_required = ['perfil.add_usuariocomite',]
    model = UsuarioComite
    form_class = ComiteUsuarioForm
    success_url = reverse_lazy('comite')

    def form_valid(self, form):
        auth_user = form['user'].save()
        user_comite = form['comiteUser'].save(commit=False)
        user_comite.usuario = auth_user
        user_comite.save()
        return HttpResponseRedirect(reverse_lazy('comite'))

    def form_invalid(self, form):
        messages.error(request, "Error")
