from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Information as ProjectInformation

# Create your views here.


class MainView(ListView):
    template_name = 'projects/pages/main.html'
    model = ProjectInformation
    context_object_name = 'projects'

    def get_queryset(self):
        user = self.request.user
        return ProjectInformation.objects.filter(
            Q(secure_level=1) |
            Q(directors__exact=user, secure_level=2) |
            Q(project_manager=user)
        ).distinct()


class InformationView(DetailView):
    template_name = 'projects/pages/information.html'
    model = ProjectInformation
    context_object_name = 'project'


class InformationCreateView(CreateView):
    template_name = 'projects/forms/information.html'
    model = ProjectInformation
    fields = ('name', 'description', 'secure_level',)

    def form_valid(self, form):
        form.instance.project_manager = self.request.user
        return super(InformationCreateView, self).form_valid(form)


class InformationUpdateView(UpdateView):
    template_name = 'projects/forms/information.html'
    model = ProjectInformation
    fields = ('name', 'description', 'secure_level',)


class InformationDirectorsUpdateView(UpdateView):
    template_name = 'projects/forms/information_directors.html'
    model = ProjectInformation
    fields = ('directors',)

    def form_valid(self, form):
        pass


class InformationDeleteView(DeleteView):
    template_name = 'projects/forms/information_delete.html'
    model = ProjectInformation
    context_object_name = 'project'
    success_url = reverse_lazy('projects-main')
