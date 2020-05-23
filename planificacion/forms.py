from django import forms
from django.forms import ClearableFileInput
from .models import Planificacion, Actividad, PagoActividad

# from betterforms.multiform import MultiModelForm
class CustomClearableFileInput(ClearableFileInput):
    template_with_clear = '<br>  <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'


class PagoActividadForm(forms.ModelForm):
    class Meta:
        model = PagoActividad
        fields = '__all__'
        widgets = {
            'factura': CustomClearableFileInput
        }