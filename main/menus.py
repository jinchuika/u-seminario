from django.core.urlresolvers import reverse_lazy
from menu import Menu, MenuItem

class ViewMenuItem(MenuItem):
    def __init__(self, *args, **kwargs):
        super(ViewMenuItem, self).__init__(*args, **kwargs)
        if 'perm' in kwargs:
            self.perm = kwargs.pop('perm')

            def check(self, request):
                """Revisa los permisos"""
                is_visible = True
                if hasattr(self, 'perm'):
                    if request.user.has_perm(self.perm):
                        is_visible = True
                    else:
                        is_visible = False
                        self.visible = is_visible


# Ventas

venta_children = (
    ViewMenuItem(
        "Nueva venta",
        reverse_lazy("venta_add"),
        icon="fa-plus"
        ),
    ViewMenuItem(
        "Listado de ventas",
        reverse_lazy("venta_all"),
        icon="fa-list"
        ),
    ViewMenuItem(
        "Actualizar precios de venta",
        reverse_lazy("venta_precio_add"),
        icon="fa-repeat"))

Menu.add_item(
    "venta",
    ViewMenuItem(
        "Ventas",
        "#",
        icon="fa-external-link",
        children=venta_children))

# Compras

compra_children = (
    ViewMenuItem(
        "Nueva compra",
        reverse_lazy("compra_add"),
        icon="fa-plus"
        ),
    ViewMenuItem(
        "Listado de compras",
        reverse_lazy("compra_all"),
        icon="fa-list"
        ),
    ViewMenuItem(
        "Actualizar precios de compra",
        reverse_lazy("compra_precio_add"),
        icon="fa-repeat"))

Menu.add_item(
    "compra",
    ViewMenuItem(
        "Compras",
        "#",
        icon="fa-level-down",
        children=compra_children))

# Inventario

producto_children = (
    ViewMenuItem(
        "Listado de productos",
        reverse_lazy("producto_all"),
        icon="fa-list"
        ),
    ViewMenuItem(
        "Agregar un producto",
        reverse_lazy("producto_add"),
        icon="fa-plus"))

Menu.add_item(
    "producto",
    ViewMenuItem(
        "Inventario",
        "#",
        icon="fa-television",
        children=producto_children))

# Administración
admin_children = (
    ViewMenuItem(
        "Análisis de datos",
        reverse_lazy("analytics"),
        weight=10,
        icon="fa-users"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Administración",
        reverse_lazy("venta_add"),
        weight=10,
        icon="fa-key",
        children=admin_children))