from django.conf.urls import url, include
from . import views
from seminario import settings
from django.contrib.auth import views as auth_views
from django.views import(
	static
	)

urlpatterns = [
    url(r'^c/$', views.CompraList.as_view(), name='compra_all'),

    url(r'^p/add/$', views.ProductoView.as_view(), name='producto_add'),
    url(r'^p/$', views.producto_all, name='producto_all'),
    url(r'^p/(?P<pk>\d+)/$', views.ProductoUpdateView.as_view(), name='producto_edit'),

    url(r'^c/add/$', views.CompraAdd.as_view(), name='compra_add'),
    url(r'^c/precio/add/$', views.PrecioCompraAdd.as_view(), name='compra_precio_add'),

    url(r'^v/add/$', views.VentaAdd.as_view(), name='venta_add'),
    url(r'^v/precio/add/$', views.PrecioVentaAdd.as_view(), name='venta_precio_add'),

    url(r'^', views.ProductoView.as_view(), name='home'),

]