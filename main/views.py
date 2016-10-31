from django.shortcuts import render, redirect, get_object_or_404
from main.models import *
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .forms import *
from .mixins import VentaContextMixin
from braces.views import LoginRequiredMixin

def compra_all(request):
	compra_list = Compra.objects.all()
	context = {
		'compra_list': compra_list
	}
	return render(request, 'compra/all.html', context)

class ProductoList(LoginRequiredMixin, ListView):
	model = Producto
	template_name = 'producto/all.html'

class ProductoView(LoginRequiredMixin, CreateView):
	model = Producto
	form_class = ProductoForm
	template_name = 'producto/add.html'
	success_url = reverse_lazy('producto_add')

	def get_context_data(self, **kwargs):
	    context = super(ProductoView, self).get_context_data(**kwargs)
	    context['producto_list'] = Producto.objects.all()
	    return context

class ProductoDetail(LoginRequiredMixin, DetailView):
	model = Producto
	template_name = 'producto/detail.html'

class PrecioVentaAdd(LoginRequiredMixin, CreateView):
	model = VentaPrecio
	form_class = VentaPrecioForm
	template_name = 'venta/precio_add.html'
	success_url = reverse_lazy('producto_add')

class PrecioCompraAdd(CreateView):
	model = CompraPrecio
	form_class = CompraPrecioForm
	template_name = 'compra/precio_add.html'
	success_url = reverse_lazy('producto_add')

class CompraAdd(CreateView):
	model = Compra
	form_class = CompraForm
	template_name = 'compra/form.html'
	success_url = reverse_lazy('compra_all')

class CompraList(LoginRequiredMixin, ListView):
	model = Compra
	template_name = 'compra/all.html'

class VentaAdd(VentaContextMixin, CreateView):
	model = Venta
	template_name = 'venta/add.html'
	success_url = reverse_lazy('producto_add')
	form_class = VentaForm

class VentaList(LoginRequiredMixin, ListView):
	model = VentaDetalle
	template_name = 'venta/all.html'

class PerfilView(LoginRequiredMixin, UpdateView):
    template_name = 'user/perfil.html'
    form_class = PerfilForm
    model = Perfil