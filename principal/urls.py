from django.urls import path
from .views import mainPage, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
from .views import revisar_sensor_proximidad
from . import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name ='login'),
    path('logout/', LogoutView.as_view(next_page ='login'), name ='logout'),
    path('register/', RegisterPage.as_view(), name ='register'),
    path('revisar_sensor_proximidad/', views.revisar_sensor_proximidad, name='revisar_sensor_proximidad'),
    path('aceptar_accion_recomendada/', views.aceptar_accion_recomendada, name='aceptar_accion_recomendada'),
    path('predecir_clima/', views.predecir_clima, name='predecir_clima'),
    path('aceptar_accion_recomendada_clima/', views.aceptar_accion_recomendada_clima, name='aceptar_accion_recomendada_clima'),
     path('asignar_estado_sensor_voltaje/', views.asignar_estado_sensor_voltaje, name='asignar_estado_sensor_voltaje'),
    path('', mainPage.as_view(), name ='mainPage')
]