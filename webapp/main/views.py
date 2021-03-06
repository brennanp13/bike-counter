#from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, UpdateView
#from django.views.generic.edit import FormView
from .models import Organization, Appointment, Membership, Location
from .logic import stats_for_appt

class OrgListView(ListView):
    model = Organization
    template_name = 'select_org.html'

    def render_to_response(self, context, **response_kwargs):
        # If there's only 1 org in the system, auto assign and move on
        if Organization.objects.all().count() > 0:  # == 1:
            org = Organization.objects.all()[0]
            mem = Membership.objects.get_or_create(user=self.request.user, organization=org)
            return HttpResponseRedirect(reverse('org_home', args=[org.slug]))
        else:
            pass

    #def get_queryset(self):
    #    pass


class OrgHomeView(DetailView):
    model = Organization
    template_name = 'org_home.html'

    def get_context_data(self, **kwargs):
        context = super(OrgHomeView, self).get_context_data(**kwargs)
        sessions = Appointment.objects.filter(user=self.request.user, organization=self.object)
        unassigned = Appointment.objects.filter(user=None, organization=self.object)
        context['sessions'] = sessions
        context['unassigned'] = unassigned
        return context


class ApptDetailView(DetailView):
    model = Appointment
    template_name = 'appointment_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ApptDetailView, self).get_context_data(**kwargs)
        context['stats'] = stats_for_appt(self.object)
        return context


class ApptCancelView(DetailView):
    model = Appointment

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == request.user:
            obj.user = None
            obj.save()
        return HttpResponseRedirect(reverse('org_home', args=[obj.organization.slug]))


class ApptSignupView(DetailView):
    model = Appointment

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect(reverse('org_home', args=[obj.organization.slug]))

class OrgScheduleView(ListView):
    model = Location
    template_name = 'org_schedule.html'

    #def render_to_response(self, context, **response_kwargs):
    #    pass

    #def get_queryset(self):
    #    pass


class ReportHomeView(ListView):
    model = Appointment
    template_name = 'report_home.html'
