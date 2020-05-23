from django import forms
from .models import UsuarioEscuela, UsuarioComite

from betterforms.multiform import MultiModelForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UsuarioEscuelaForm(forms.ModelForm):
    class Meta:
        model = UsuarioEscuela
        fields = '__all__'

class UsuarioComiteForm(forms.ModelForm):
    class Meta:
        model = UsuarioComite
        fields = '__all__'

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

class EscuelaUsuarioForm(MultiModelForm):
    form_classes = {
        'usuario': UsuarioEscuelaForm,
        'user': SignUpForm,
    }

class ComiteUsuarioForm(MultiModelForm):
    form_classes = {
        'comiteUser': UsuarioComiteForm,
        'user': SignUpForm,
    }