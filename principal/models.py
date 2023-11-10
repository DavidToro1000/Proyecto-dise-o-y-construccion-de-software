from django.db import models

from django.db import models
import random



# Definimos la clase Sector, que representa un sector en el que se pueden encontrar dispositivos de iluminación
class Sector(models.Model):
    # El nombre del sector, que también actúa como su clave primaria
    nombre = models.CharField(max_length=50, primary_key=True)

    # Método para convertir un objeto Sector a string
    def __str__(self):
        return self.nombre

# Definimos la clase DispositivoIluminacion, que representa un dispositivo de iluminación
class DispositivoIluminacion(models.Model):

    # Definimos las posibles opciones para el estado de un dispositivo de iluminación
    ESTADO_CHOICES = [
        ('apagado', 'Apagado'),
        ('encendido', 'Encendido'),
    ]

    # Definimos las posibles opciones para la luminosidad de un dispositivo de iluminación
    LUMINOSIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('alta', 'Alta'),
    ]

    # Definimos las posibles opciones para el voltaje de un dispositivo de iluminación
    VOLTAJE_CHOICES = [
        ('bajo', 'Bajo'),
        ('normal', 'Normal'),
        ('alto', 'Alto'),
    ]

    # El id del dispositivo de iluminación, que actúa como su clave primaria
    id = models.AutoField(primary_key=True)
    # El estado del sensor de proximidad del dispositivo de iluminación
    estado_sensor_proximidad = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    # El estado del sensor de voltaje del dispositivo de iluminación
    estado_sensor_voltaje = models.CharField(max_length=10, choices=VOLTAJE_CHOICES)
    # La luminosidad del dispositivo de iluminación
    luminosidad = models.CharField(max_length=10, choices=LUMINOSIDAD_CHOICES)
    # Las políticas de iluminación del dispositivo de iluminación
    politicas_iluminacion = models.TextField()
    # El sector al que pertenece el dispositivo de iluminación
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    # Método para generar un estado de sensor de voltaje aleatorio
    def generar_estado_sensor_voltaje_aleatorio(self):
        estado = random.choices(
            ['normal', 'bajo', 'alto'],
            weights=[0.9, 0.05, 0.05],
            k=1
        )[0]
        self.estado_sensor_voltaje = estado
        self.save()

    # Método para generar un estado de sensor de proximidad aleatorio
    def generar_estado_sensor_proximidad_aleatorio(self):
        self.estado_sensor_proximidad = random.choice(self.ESTADO_CHOICES)[0]
        self.save()

    # Método para establecer la luminosidad a 'alta'
    def establecer_luminosidad_alta(self):
        self.luminosidad = 'alta'
        self.save()

    # Método para establecer la luminosidad a 'baja'
    def establecer_luminosidad_baja(self):
        self.luminosidad = 'baja'
        self.save()
    
    # Método para verificar si el dispositivo de iluminación está encendido y en un sector
    def esta_encendido_en_sector(self):
        # Devuelve True si el estado del sensor de proximidad es 'encendido' y el dispositivo está en un sector
        return self.estado_sensor_proximidad == 'encendido' and self.sector is not None

    # Método para convertir un objeto DispositivoIluminacion a string
    def __str__(self):
        # Devuelve una cadena que contiene el id del dispositivo, el sector al que pertenece y su luminosidad
        return f"{self.id} - {self.sector} - {self.luminosidad}"