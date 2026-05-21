from django.contrib import admin
from .models import Ubicacion, Evento, PrecioCategoria


class PrecioCategoriaInline(admin.TabularInline):
    model = PrecioCategoria
    extra = 1


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'capacidad_maxima')
    search_fields = ('nombre', 'ciudad')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'organizador', 'ubicacion', 'fecha_inicio', 'estado', 'entradas_vendidas')
    list_filter = ('estado', 'fecha_inicio')
    search_fields = ('titulo', 'organizador__username')
    inlines = [PrecioCategoriaInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PrecioCategoria)
class PrecioCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'evento', 'precio', 'cantidad_disponible', 'vendidas', 'disponibles')
    list_filter = ('evento',)
