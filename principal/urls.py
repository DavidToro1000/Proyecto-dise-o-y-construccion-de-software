from django.urls import path
from .views import mainPage, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
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
    path('revisar_notificacion_trafico/', views.revisar_notificacion_trafico, name='revisar_notificacion_trafico'),
    path('revisar_notificacion_emergencia/', views.revisar_notificacion_emergencia, name='revisar_notificacion_emergencia'),
    path('ajustar_trafico_vehiculos_emergencia/', views.ajustar_trafico_vehiculos_emergencia, name='ajustar_trafico_vehiculos_emergencia'),
    path('revisar_estado_luminosidad/', views.revisar_estado_luminosidad, name='revisar_estado_luminosidad'),
    path('aceptar_accion_recomendada_luminosidad/', views.aceptar_accion_recomendada_luminosidad, name='aceptar_accion_recomendada_luminosidad'),
    path('revisar_notificacion_vial/', views.revisar_notificacion_vial, name='revisar_notificacion_vial'),
    path('ajustar_via_alterna/', views.ajustar_via_alterna, name='ajustar_via_alterna'),
    path('', mainPage.as_view(), name ='mainPage')
]