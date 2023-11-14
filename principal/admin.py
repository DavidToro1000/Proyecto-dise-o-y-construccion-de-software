from django.contrib import admin

from .models import Sector
from .models import DispositivoIluminacion, SistemaTrafico, ProveedorServiciosDeEmergencia
admin.site.register(Sector)
admin.site.register(DispositivoIluminacion)
admin.site.register(SistemaTrafico)
admin.site.register(ProveedorServiciosDeEmergencia)

# Register your models here.
