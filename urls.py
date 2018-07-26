from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import MainView as ProjectMainView
from .views import InformationView as ProjectInformationView
from .views import InformationCreateView as ProjectInformationCreateView
from .views import InformationUpdateView as ProjectInformationUpdateView
from .views import InformationDeleteView as ProjectInformationDeleteView
from .views import InformationDirectorsUpdateView as ProjectInformationDirectorsUpdateView

# Create your urls here.
urlpatterns = [
    path('', login_required(ProjectMainView.as_view()), name='projects-main'),
    path('new/', login_required(ProjectInformationCreateView.as_view()),
         name='project-create'),
    path('<pk>/update/', login_required(ProjectInformationUpdateView.as_view()),
         name='project-update'),
    path('<pk>/delete/', login_required(ProjectInformationDeleteView.as_view()),
         name='project-delete'),
    path('<pk>/directors/', login_required(ProjectInformationDirectorsUpdateView.as_view()),
         name='project-directors'),
    path('<pk>/detail/', login_required(ProjectInformationView.as_view(template_name='projects/pages/information.html')),
         name='project-information'),
    path('<pk>/tasks/', login_required(),
         name='project-tasks'),
]
