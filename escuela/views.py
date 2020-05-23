from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from core.views import SinPrivilegios

from .models import Escuela
from core.models import Departamento, Municipio

from .forms import EscuelaForm, EscuelaUpdateForm, SignUpForm, EscuelaUsuarioForm

# Create your views here.

class EscuelaCreate(SinPrivilegios, CreateView):
    permission_required = ['escuela.view_escuela', 'escuela.add_escuela']
    model = Escuela
    form_class = EscuelaForm
    success_url = reverse_lazy('list_escuela')

# Listado de Escuelas
class EscuelaListView(SinPrivilegios, ListView):
    permission_required = ['escuela.view_escuela', 'escuela.add_escuela']
    model = Escuela
    context = 'list_objects'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super(EscuelaListView, self).get_context_data(**kwargs)
        context.update(**kwargs)
        dato = None
        usuario = self.request.user
        context['escuela'] = Escuela.objects.all()
        context['depto'] = Departamento.objects.all()
        context['muni'] = Municipio.objects.filter(departamento=dato)
        return context

# Vista ajax para devolver los municipios
def load_municipios(request):
    departamento_id = request.GET.get('depto')
    print(departamento_id)
    municipio = Municipio.objects.filter(departamento=departamento_id).order_by('codigo')
    return render(request, 'escuela/include/municipio_dropdown_list_options.html', {'municipio': municipio})

class EscuelaDelete(SinPrivilegios, DeleteView):
    permission_required = ['escuela.view_escuela', 'escuela.add_escuela']
    model = Escuela
    success_url = reverse_lazy('list_escuela')

class EscuelaUpdate(SinPrivilegios, UpdateView):
    permission_required = ['escuela.view_escuela', 'escuela.add_escuela']
    model = Escuela
    form_class = EscuelaUpdateForm
    template_name = 'escuela/escuela_form.html'
    success_url = reverse_lazy('list_escuela')