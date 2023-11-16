from django.contrib import admin

from .models import Sector
from .models import DispositivoIluminacion, SistemaTrafico, ProveedorServiciosDeEmergencia, SistemaMantenimientoVial
admin.site.register(Sector)
admin.site.register(DispositivoIluminacion)
admin.site.register(SistemaTrafico)
admin.site.register(ProveedorServiciosDeEmergencia)
admin.site.register(SistemaMantenimientoVial)

# Register your models here.
