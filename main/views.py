from django.shortcuts import render, redirect, get_object_or_404
from main.models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import ProductoForm, VentaPrecioForm, CompraPrecioForm
from .mixins import PrecioMixin

def compra_all(request):
	compra_list = Compra.objects.all()
	context = {
		'compra_list': compra_list
	}
	return render(request, 'compra/all.html', context)

def producto_all(request):
	producto_list = Producto.objects.all()
	context = {
		'producto_list': producto_list
	}
	return render(request, 'producto/all.html', context)

class ProductoView(CreateView):
	model = Producto
	form_class = ProductoForm
	template_name = 'producto/add.html'
	success_url = reverse_lazy('producto_add')

	def get_context_data(self, **kwargs):
	    context = super(ProductoView, self).get_context_data(**kwargs)
	    context['producto_list'] = Producto.objects.all()
	    return context

class ProductoUpdateView(PrecioMixin, UpdateView):
	model = Producto
	form_class = ProductoForm
	template_name = 'producto/detail.html'
	success_url = reverse_lazy('producto_add')

class PrecioVentaAdd(CreateView):
	model = VentaPrecio
	form_class = VentaPrecioForm
	template_name = 'venta/precio_add.html'
	success_url = reverse_lazy('producto_all')

class PrecioCompraAdd(CreateView):
	model = CompraPrecio
	form_class = CompraPrecioForm
	template_name = 'compra/precio_add.html'
	success_url = reverse_lazy('producto_add')