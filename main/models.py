import os
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import timedelta, date, time
from django.utils import timezone

class Trabajador(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name

class Producto(models.Model):
	nombre = models.CharField(max_length=150)

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
	producto = models.ForeignKey('Producto')
	cantidad = models.IntegerField()
	fecha = models.DateField(default=timezone.now)

	def precio(self):
		if self.producto.precio_compra_actual:
			return self.producto.precio_compra_actual.precio
		else:
			return 0
	precio = property(precio)

	def total(self):
		return self.cantidad * self.precio

	def __str__(self):
		return str(self.producto) + str(self.fecha)

class CompraPrecio(models.Model):
	producto = models.ForeignKey('Producto', related_name='precio_compra')
	precio = models.DecimalField(max_digits=9, decimal_places=2)
	fecha = models.DateField(default=timezone.now)

	class Meta:
		unique_together = ('producto', 'fecha')


	def __str__(self):
		return str(self.precio)
		

class Venta(models.Model):
	vendedor = models.ForeignKey('Trabajador')
	fecha = models.DateField(default=timezone.now)

	def __str__(self):
		return str(self.fecha) + str(self.id)

class VentaPrecio(models.Model):
	producto = models.ForeignKey('Producto', related_name='precio_venta')
	precio = models.DecimalField(max_digits=9, decimal_places=2)
	fecha = models.DateField(default=timezone.now)
	
	class Meta:
		unique_together = ('producto', 'fecha')

	def __str__(self):
		return str(self.precio)

class VentaDetalle(models.Model):
	venta = models.ForeignKey('Venta')
	producto = models.ForeignKey('Producto')
	cantidad = models.IntegerField()

	def precio(self):
		return self.producto.precio_venta_actual()
	precio = property(precio)

	def total(self):
		return self.cantidad * self.precio()

	def __str__(self):
		return str(self.producto) + str(self.cantidad)