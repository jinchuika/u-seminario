from django.shortcuts import render, redirect, get_object_or_404
from main.models import *
from datetime import timedelta, date, time
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth import authenticate, login
from django.views.generic import View

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