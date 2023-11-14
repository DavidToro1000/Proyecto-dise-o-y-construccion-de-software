from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.http import JsonResponse
from django.shortcuts import render
from .models import DispositivoIluminacion, Sector, SistemaTrafico, ProveedorServiciosDeEmergencia
from django.views.decorators.csrf import csrf_exempt
import random

#Creacion del sistema de tráfico
sistemaTrafico = SistemaTrafico()
sistemaTrafico.contacto = "trafico@trabajo.com"
sistemaTrafico.save()

#Creacion del proveedor de servicios de emergencia
sistemaTrafico = ProveedorServiciosDeEmergencia()
sistemaTrafico.contacto = "proveedorEmergencia@trabajo.com"
sistemaTrafico.save()

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('mainPage')

class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('mainPage')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
         return redirect('mainPage')
        return super(RegisterPage, self).get(*args, **kwargs)
     
class mainPage(View, LoginRequiredMixin):
    template_name = 'mainPage.html'

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return render(request, self.template_name, {})
    
# Definimos la vista para revisar el sensor de proximidad
@csrf_exempt
def revisar_sensor_proximidad(request):
    # Si la petición es POST
    if request.method == 'POST':
        # Obtenemos todos los dispositivos de iluminación
        dispositivos = DispositivoIluminacion.objects.all()
        # Para cada dispositivo, generamos un estado de sensor de proximidad aleatorio
        for dispositivo in dispositivos:
            dispositivo.generar_estado_sensor_proximidad_aleatorio()

        # Obtenemos los sectores donde los dispositivos de iluminación tienen el sensor de proximidad encendido
        sectores = Sector.objects.filter(dispositivoiluminacion__estado_sensor_proximidad='encendido').distinct()
        # Obtenemos los nombres de estos sectores
        sectores_nombres = [sector.nombre for sector in sectores]
        # Devolvemos los nombres de los sectores en formato JSON
        return JsonResponse({'sectores': sectores_nombres})

# Definimos la vista para aceptar la acción recomendada
@csrf_exempt
def aceptar_accion_recomendada(request):
    # Si la petición es POST
    if request.method == 'POST':
        # Obtenemos los sectores donde los dispositivos de iluminación tienen el sensor de proximidad encendido
        sectores = Sector.objects.filter(dispositivoiluminacion__estado_sensor_proximidad='encendido').distinct()
        # Para cada sector
        for sector in sectores:
            # Obtenemos los dispositivos de iluminación de ese sector
            dispositivos = sector.dispositivoiluminacion_set.all()
            # Para cada dispositivo, establecemos la luminosidad a alta
            for dispositivo in dispositivos:
                dispositivo.establecer_luminosidad_alta()
        # Devolvemos un mensaje de éxito en formato JSON
        return JsonResponse({'message': 'Acción realizada con éxito.'})

    
# Definimos la vista para predecir el clima
@csrf_exempt
def predecir_clima(request):
    # Si la petición es POST
    if request.method == 'POST':
        # Generamos un clima aleatorio
        clima = random.choice(['Tormenta', 'Amanecer', 'Atardecer', 'Despejado'])
        # Obtenemos todos los sectores
        sectores = Sector.objects.all()
        # Elegimos un sector aleatorio
        sector = random.choice(sectores)
        # Devolvemos el clima y el nombre del sector en formato JSON
        return JsonResponse({'clima': clima, 'sector': sector.nombre})

# Definimos la vista para aceptar la acción recomendada en función del clima
@csrf_exempt
def aceptar_accion_recomendada_clima(request):
    # Si la petición es POST
    if request.method == 'POST':
        # Obtenemos el clima y el nombre del sector de la petición
        clima = request.POST.get('clima')
        sector_nombre = request.POST.get('sector')
        # Obtenemos el sector por su nombre
        sector = Sector.objects.get(nombre=sector_nombre)
        # Obtenemos los dispositivos de iluminación de ese sector
        dispositivos = sector.dispositivoiluminacion_set.all()
        # Si el clima es 'Amanecer', establecemos la luminosidad de los dispositivos a baja
        if clima == 'Amanecer':
            for dispositivo in dispositivos:
                dispositivo.establecer_luminosidad_baja()
        # Si el clima es 'Tormenta' o 'Atardecer', establecemos la luminosidad de los dispositivos a alta
        elif clima in ['Tormenta', 'Atardecer']:
            for dispositivo in dispositivos:
                dispositivo.establecer_luminosidad_alta()
        # Si el clima es 'Despejado', no hacemos nada y devolvemos un mensaje
        else:
            return JsonResponse({'message': 'No se detecta un cambio de clima que requiera acción.'})
        # Devolvemos un mensaje de éxito en formato JSON
        return JsonResponse({'message': 'Acción realizada con éxito.'})

# Definimos la vista para asignar el estado del sensor de voltaje
def asignar_estado_sensor_voltaje(request):
    # Obtenemos todos los dispositivos de iluminación
    dispositivos = DispositivoIluminacion.objects.all()
    # Para cada dispositivo, generamos un estado de sensor de voltaje aleatorio
    for dispositivo in dispositivos:
        dispositivo.generar_estado_sensor_voltaje_aleatorio()
    # Si algún dispositivo tiene un estado de sensor de voltaje que no es 'normal', devolvemos una alerta
    if any(dispositivo.estado_sensor_voltaje != 'normal' for dispositivo in dispositivos):
        return JsonResponse({'message': 'Alerta! Niveles de voltaje anormales. Notifique al proveedor de servicios de electricidad.', 'alert': True})
    # Si todos los dispositivos tienen un estado de sensor de voltaje 'normal', devolvemos un mensaje
    else:
        return JsonResponse({'message': 'Todos los dispositivos de iluminación presentan niveles de voltaje normales.', 'alert': False})
    
# Funcion para verificar si existe alguna notificacion del sistema de trafico
@csrf_exempt
def revisar_notificacion_trafico(request):
    # Si la petición es POST
    if request.method == 'POST':
        # Para simular la notificacion se introduce un random de modo que el 30% de las veces si exista una notificacion
        if random.random() <=0.3:
            # Obtenemos todos los dispositivos de iluminación
            dispositivos = DispositivoIluminacion.objects.all()
            # Para cada dispositivo, generamos un estado de sensor de proximidad aleatorio
            for dispositivo in dispositivos:
                dispositivo.generar_estado_sensor_proximidad_aleatorio()

            # Obtenemos los sectores donde los dispositivos de iluminación tienen el sensor de proximidad encendido
            sectores = Sector.objects.filter(dispositivoiluminacion__estado_sensor_proximidad='encendido').distinct()
            # Obtenemos los nombres de estos sectores
            sectores_nombres = [sector.nombre for sector in sectores]
            #Traemos el sistema de trafico para llamar el metodo notificar
            trafico = SistemaTrafico.objects.all()
            trafico = trafico[0] #solo debe haber un sistema de trafico
            notificacion = trafico.notificarCruce(sectores_nombres)
            # Devolvemos los nombres de los sectores en formato JSON
            return JsonResponse({"alerta": True, "notificacion": notificacion})
        else:
            return JsonResponse({"alerta": False, "notificacion": "No hay notificaciones del sistema de trafico."})
        
# Definimos la vista para ajustar las luces para trafico de vehiculos de emergencia
@csrf_exempt
def ajustar_trafico_vehiculos_emergencia(request):
    # Si la petición es POST
    if request.method == 'POST':
        # Obtenemos los sectores donde los dispositivos de iluminación tienen el sensor de proximidad encendido
        sectores = Sector.objects.filter(dispositivoiluminacion__estado_sensor_proximidad='encendido').distinct()
        # Para cada sector
        for sector in sectores:
            # Obtenemos los dispositivos de iluminación de ese sector
            dispositivos = sector.dispositivoiluminacion_set.all()
            # Para cada dispositivo, establecemos la luminosidad a alta
            for dispositivo in dispositivos:
                dispositivo.establecer_luminosidad_alta()
        # Devolvemos un mensaje de éxito en formato JSON
        return JsonResponse({'message': 'Acción realizada con éxito.'})
    
# Funcion para verificar si existe alguna notificacion del proveedor de servicios de emergencia
@csrf_exempt
def revisar_notificacion_emergencia(request):
    # Si la petición es POST
    if request.method == 'POST':
        # Para simular la notificacion se introduce un random de modo que el 30% de las veces si exista una notificacion
        if random.random() <=0.3:
            # Obtenemos todos los dispositivos de iluminación
            dispositivos = DispositivoIluminacion.objects.all()
            # Para cada dispositivo, generamos un estado de sensor de proximidad aleatorio
            for dispositivo in dispositivos:
                dispositivo.generar_estado_sensor_proximidad_aleatorio()

            # Obtenemos los sectores donde los dispositivos de iluminación tienen el sensor de proximidad encendido
            sectores = Sector.objects.filter(dispositivoiluminacion__estado_sensor_proximidad='encendido').distinct()
            # Obtenemos los nombres de estos sectores
            sectores_nombres = [sector.nombre for sector in sectores]
            #Traemos el proveedor para llamar el metodo notificar
            emergencia = ProveedorServiciosDeEmergencia.objects.all()
            emergencia = emergencia[0] #solo debe haber un proveedor
            notificacion = emergencia.notificarVehiculo(sectores_nombres)
            # Devolvemos los nombres de los sectores en formato JSON
            return JsonResponse({"alerta": True, "notificacion": notificacion})
        else:
            return JsonResponse({"alerta": False, "notificacion": "No hay notificaciones del proveedor de servicios de emergencia."})