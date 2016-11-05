import os
from django.db import models
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import timedelta, date, time
from django.utils import timezone

from easy_thumbnails.fields import ThumbnailerImageField

class Perfil(models.Model):
    GENERO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dpi = models.CharField(max_length=20, unique=True)
    public = models.BooleanField(default=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='M')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    foto = ThumbnailerImageField(
        upload_to="perfil_usuario",
        null=True,
        blank=True,
        editable=True,)
    objects = models.Manager()

    def get_nombre(self):
        return self.user.first_name
    nombre = property(get_nombre)

    def get_apellido(self):
        return self.user.last_name
    apellido = property(get_apellido)

    def get_absolute_url(self):
        return reverse_lazy('perfil', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        return self.nombre + " " + self.apellido

class Producto(models.Model):
    nombre = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse_lazy('producto_detail', kwargs={'pk': self.id})

    def precio_compra_actual(self, fecha=date.today()):
        ultimo_precio = CompraPrecio.objects.filter(fecha__lte=fecha, producto=self).order_by('fecha').reverse()
        if ultimo_precio.count() < 1:
            return None
        else:
            return ultimo_precio[0]
    precio_compra_actual = property(precio_compra_actual)

    def precio_venta_actual(self,fecha=date.today()):
        ultimo_precio = VentaPrecio.objects.filter(fecha__lte=fecha, producto=self).order_by('fecha').reverse()
        if ultimo_precio.count() < 1:
            return None
        else:
            return ultimo_precio[0]
    precio_venta_actual = property(precio_venta_actual)

    def compras(self):
        compra_list = Compra.objects.filter(producto=self)
        if compra_list.count() < 1:
            return 0
        else:
            return sum(compra.cantidad for compra in compra_list)
    compras = property(compras)

    def ventas(self):
        venta_list = VentaDetalle.objects.filter(producto=self)
        if venta_list.count() < 1:
            return 0
        else:
            return sum(venta.cantidad for venta in venta_list)
    ventas = property(ventas)

    def existencia(self):
        return self.compras - self.ventas
    existencia = property(existencia)

    def __str__(self):
        return str(self.nombre)

class Compra(models.Model):
    producto = models.ForeignKey('Producto', related_name='compra')
    cantidad = models.IntegerField()
    fecha = models.DateField(default=timezone.now)

    def get_precio(self):
        precio = CompraPrecio.objects.filter(producto=self.producto, fecha__lte=self.fecha).order_by('fecha').last()
        if precio:
            return precio.precio
        else:
            return 0
        
    precio = property(get_precio)

    def total(self):
        return self.cantidad * self.precio

    def __str__(self):
        return "No. " + str(self.id) + " - (" + str(self.fecha) + ")"

class CompraPrecio(models.Model):
    producto = models.ForeignKey('Producto', related_name='precio_compra')
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    fecha = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('producto', 'fecha')


    def __str__(self):
        return str(self.producto)+ " - " + str(self.fecha) + " - " + str(self.precio)
        

class Venta(models.Model):
    vendedor = models.ForeignKey('Perfil')
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return "No. " + str(self.id) + " - (" + str(self.fecha) + ")"

class VentaPrecio(models.Model):
    producto = models.ForeignKey('Producto', related_name='precio_venta')
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    fecha = models.DateField(default=timezone.now)
    
    class Meta:
        unique_together = ('producto', 'fecha')

    def __str__(self):
        return str(self.precio)

class VentaDetalle(models.Model):
    venta = models.ForeignKey('Venta', related_name='detalle_venta')
    producto = models.ForeignKey('Producto', related_name='venta')
    cantidad = models.IntegerField()

    def get_precio(self):
        precio = VentaPrecio.objects.filter(producto=self.producto, fecha__lte=self.venta.fecha).order_by('fecha').last()
        if precio:
            return precio.precio
        else:
            return 0

    precio = property(get_precio)

    def total(self):
        return self.cantidad * self.precio

    def __str__(self):
        return str(self.producto) + " - " + str(self.cantidad)