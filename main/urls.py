from django.conf.urls import url, include
from . import views
from seminario import settings
from django.contrib.auth import views as auth_views
from django.views import(
	static
	)

urlpatterns = [
    url(r'^c/$', views.compra_all, name='compra_all'),

    url(r'^p/$', views.producto_all, name='producto_all'),
]