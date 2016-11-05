import json
from django.http import HttpResponse
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from main.models import *
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from main.forms import *
from main.mixins import VentaContextMixin
from main.bi import *
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

    def form_valid(self, form):
        form.instance.vendedor = self.request.user.perfil
        return super(VentaAdd, self).form_valid(form)


class VentaList(LoginRequiredMixin, ListView):
    model = VentaDetalle
    template_name = 'venta/all.html'


class PerfilView(LoginRequiredMixin, UpdateView):
    template_name = 'user/perfil.html'
    form_class = PerfilForm
    model = Perfil

class Analytics(LoginRequiredMixin, TemplateView):
    template_name = "bi/home.html"
    def get_context_data(self, **kwargs):
        context = super(Analytics, self).get_context_data(**kwargs)
        resumen = []
        mes = Calendario().get_mes_actual()
        for dia in mes:
            resumen.append({
                'dia': dia,
                'ventas': Venta.objects.filter(fecha=dia),
                'compras': Compra.objects.filter(fecha=dia),
                })
        context['resumen'] = resumen
        return context

class AnalyticsApi(LoginRequiredMixin, TemplateView):
    def get(self, request):
        qs = self.analyze_producto(request.GET.get('inicio', None), request.GET.get('fin', None))

        return HttpResponse(
            json.dumps(qs)
            )

    def analyze_producto(self, fecha_inicio=None, fecha_fin=None):
        venta_list = Venta.objects.all()
        compra_list = Compra.objects.all()
        if fecha_inicio:
            venta_list = venta_list.filter(fecha__gte=fecha_inicio)
            compra_list = compra_list.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            venta_list = venta_list.filter(fecha__lte=fecha_fin)
            compra_list = compra_list.filter(fecha__lte=fecha_fin)

        producto_list = Producto.objects.all()

        lista = []
            

        for producto in producto_list:
            lista.append({
                'producto': producto.nombre,
                'cantidad': sum(venta.cantidad for venta in producto.venta.filter(venta__in=venta_list)),
                'cantidad_compra': sum(compra.cantidad for compra in producto.compra.filter(fecha__range=[fecha_inicio, fecha_fin])),
                })
        return lista