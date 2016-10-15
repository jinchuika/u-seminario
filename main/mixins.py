from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from .forms import VentaForm, VentaDetalleFormSet

class VentaContextMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(VentaContextMixin, self).get_context_data(**kwargs)
		context['named_formsets'] = self.get_named_formsets()
		return context

	def get_named_formsets(self):
		return {
			'detalle': VentaDetalleFormSet(self.request.POST or None, prefix='detalle', instance = self.object),
		}

	def form_valid(self, form):
		named_formsets = self.get_named_formsets()
		if not all((x.is_valid() for x in named_formsets.values())):
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

	def formset_detalle_valid(self, formset):
		detalles = formset.save(commit=False)
		print(detalles)
		for obj in formset.deleted_objects:
			obj.delete()

		for detalle in detalles:
			print(detalle)
			detalle.venta = self.object
			detalle.save()