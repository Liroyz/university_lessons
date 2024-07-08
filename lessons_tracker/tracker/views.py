from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic import TemplateView, ListView

from .forms import CustomUserCreationForm, ScheduleForm, ScheduleFilterForm
from .mixins import TeacherRequiredMixin
from .models import Schedule


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


class ScheduleListView(ListView):
    model = Schedule
    template_name = 'tracker/schedule_list.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ScheduleFilterForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            date = form.cleaned_data.get('date')
            teacher = form.cleaned_data.get('teacher')
            if search:
                queryset = queryset.filter(title__icontains=search)
            if date:
                queryset = queryset.filter(date=date)
            if teacher:
                queryset = queryset.filter(teacher__username__icontains=teacher)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ScheduleFilterForm(self.request.GET)
        return context


class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = 'tracker/schedule_detail.html'
    context_object_name = 'schedule'


class ScheduleCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'tracker/schedule_form.html'
    success_url = reverse_lazy('schedule_list')


class ScheduleUpdateView(TeacherRequiredMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'tracker/schedule_form.html'
    success_url = reverse_lazy('schedule_list')

