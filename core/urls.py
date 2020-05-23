from django.urls import path
from django.contrib.auth import views as auth_views
from .views import DepartamentoListView, Home, HomeSinPrivilegios

urlpatterns = [
	path('login/', auth_views.LoginView.as_view(template_name="core/login.html"), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name="core/login.html"), name='logout'),
    path('', Home.as_view(), name='home'),
    path('NoPermitido/', HomeSinPrivilegios.as_view(), name='sin_privilegios'),
]
