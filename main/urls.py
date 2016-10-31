from django.conf.urls import url, include
from . import views
from seminario import settings
from django.contrib.auth import views as auth_views
from django.views import(
	static
	)

urlpatterns = [
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^c/$', views.CompraList.as_view(), name='compra_all'),

    url(r'^p/(?P<pk>\d+)/$', views.ProductoDetail.as_view(), name='producto_detail'),
    url(r'^p/add/$', views.ProductoView.as_view(), name='producto_add'),
    url(r'^p/$', views.ProductoList.as_view(), name='producto_all'),

    url(r'^c/add/$', views.CompraAdd.as_view(), name='compra_add'),
    url(r'^c/precio/add/$', views.PrecioCompraAdd.as_view(), name='compra_precio_add'),

    url(r'^v/add/$', views.VentaAdd.as_view(), name='venta_add'),
    url(r'^v/precio/add/$', views.PrecioVentaAdd.as_view(), name='venta_precio_add'),
    url(r'^v/$', views.VentaList.as_view(), name='venta_all'),

    url(r'^perfil/(?P<pk>\d+)/$', views.PerfilView.as_view(), name='perfil'),

    url(r'^$', views.ProductoView.as_view(), name='home'),

]