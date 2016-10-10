from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from .forms import PrecioCompraFormSet, PrecioVentaFormSet
from datetime import date

class PrecioMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(PrecioMixin, self).get_context_data(**kwargs)
		context['named_formsets'] = self.get_named_formsets()
		return context

	def get_named_formsets(self):
		return {
			'compra': PrecioCompraFormSet(self.request.POST or None, prefix='compra', instance = self.object),
			'venta': PrecioVentaFormSet(self.request.POST or None, prefix='venta', instance = self.object),
		}

	def form_valid(self, form):
		named_formsets = self.get_named_formsets()
		if not all((x.is_valid() for x in named_formsets.values())):
			for x in named_formsets.values():
				print(x.errors)
			return self.render_to_response(self.get_context_data(form=form))
		else:
			self.object = form.save()

		for name, formset in named_formsets.items():
			formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
			if formset_save_func is not None:
				formset_save_func(formset)
			else:
				formset.save()
		return redirect(self.success_url)

	def formset_compra_valid(self, formset):
		compras = formset.save(commit=False)
		print(compras)
		for obj in formset.deleted_objects:
			obj.delete()

		for compra in compras:
			print(compra)
			compra.producto = self.object
			compra.fecha = date.today()
			compra.save()

	def formset_venta_valid(self, formset):
		ventas = formset.save(commit=False)
		for obj in formset.deleted_objects:
			obj.delete()
		for venta in ventas:
			venta.producto = self.object
			venta.fecha = date.today()
			venta.save()