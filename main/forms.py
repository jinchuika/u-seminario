from django import forms
from django.forms import ModelForm, ValidationError
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

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'

    def clean(self):
        cleaned_data = super(CompraForm, self).clean()
        if CompraPrecio.objects.filter(producto=cleaned_data['producto']).count() == 0:
            raise forms.ValidationError(
                 "El producto aún no tiene un precio de compra asignado"
                )

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        exclude = ('vendedor',)


VentaDetalleFormSet = inlineformset_factory(Venta, VentaDetalle, fields='__all__',extra=1, can_delete=False)
PrecioVentaFormSet = inlineformset_factory(Producto, VentaPrecio, fields='__all__',extra=1, can_delete=False)


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ('user', 'public')