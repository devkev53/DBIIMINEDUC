from django import forms
from .models import Integrante

from betterforms.multiform import MultiModelForm

from padre.models import PadreFamilia


class IntegranteComiteForm(forms.ModelForm):
    class Meta:
        model = Integrante
        fields = '__all__'

class PersonaForm(forms.ModelForm):
    class Meta:
        model = PadreFamilia
        fields = '__all__'

class IntegranteForm(MultiModelForm):
    form_classes = {
        'integrante': IntegranteComiteForm,
        'persona': PersonaForm,
    }
