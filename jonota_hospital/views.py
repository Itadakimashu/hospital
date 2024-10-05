from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from doctor.models import Doctor,Specialization

class Homepage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        specialization_slug = self.request.GET.get('specialization')

        if specialization_slug:
            specialization = get_object_or_404(Specialization, slug=specialization_slug)
            context['doctors'] = Doctor.objects.filter(specialization=specialization)
        else:
            context['doctors'] = Doctor.objects.all()
            
        context['specializations'] = Specialization.objects.all()
        return context

