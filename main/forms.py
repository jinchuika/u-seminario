from django import forms
from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory

class ProductoForm(forms.ModelForm):
	class Meta:
		model = Producto
		fields = '__all__'
		widgets = {
		'nombre': forms.TextInput(attrs={'class': 'form-control border-input'})
		}

class VentaPrecioForm(ModelForm):
	class Meta:
		model = VentaPrecio
		fields = ('producto', 'precio',)
		widgets = {
		'producto': forms.Select(attrs={'class': 'form-control border-input'}),
		'precio': forms.NumberInput(attrs={'class': 'form-control border-input'}),
		}

class CompraPrecioForm(ModelForm):
	class Meta:
		model = CompraPrecio
		fields = ('producto', 'precio',)
		widgets = {
		'producto': forms.Select(attrs={'class': 'form-control border-input'}),
		'precio': forms.NumberInput(attrs={'class': 'form-control border-input'}),
		}
						

PrecioCompraFormSet = inlineformset_factory(Producto, CompraPrecio, fields='__all__',extra=1, can_delete=False)
PrecioVentaFormSet = inlineformset_factory(Producto, VentaPrecio, fields='__all__',extra=1, can_delete=False)