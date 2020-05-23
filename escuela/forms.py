from django import forms
from .models import Escuela
from core.models import Municipio

from betterforms.multiform import MultiModelForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class EscuelaForm(forms.ModelForm):
    class Meta:
        model = Escuela
        fields = [
        	'codigo', 'nombre', 'direccion', 'departamento', 'municipio'
        	]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['municipio'].queryset = Municipio.objects.none()
        self.fields['codigo'].widget.attrs['readonly'] = True
        self.fields['codigo'].widget.attrs['display'] = None

        if 'departamento' in self.data:
        	try:
        		departamento_id = str(self.data.get('departamento'))
        		self.fields['municipio'].queryset = Municipio.objects.filter(departamento=departamento_id).order_by('codigo')
        	except (ValueError, TypeError):
        		pass


class EscuelaUpdateForm(forms.ModelForm):
    class Meta:
        model = Escuela
        fields = [
            'codigo', 'nombre', 'direccion'
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['readonly'] = True


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

class EscuelaUsuarioForm(MultiModelForm):
    form_classes = {
        'escuela': EscuelaForm,
        'usuario': SignUpForm,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['municipio'].queryset = Municipio.objects.filter(departamento=departamento_id).order_by('codigo')
            except (ValueError, TypeError):
                pass