from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from .models import BranchOffices, Patients, Personel, Visits, getAllVisits
from .forms import BranchOfficesForm, PatientsForm, PersonelForm, VisitsForm, UserForm, ChangePasswordForm
from django.dispatch import receiver
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save


def home(request):
    return render(request, 'home.html')


def branch_offices_list(request):
    branch_offices = BranchOffices.objects.all()
    return render(request, 'branch_offices_list.html', {'branch_offices': branch_offices})


class BranchOfficeDetail(DetailView):
    model = BranchOffices
    template_name = 'branch_offices_detail.html'


class BranchOfficeUpdate(PermissionRequiredMixin, UpdateView):
    model = BranchOffices
    fields = '__all__'
    template_name = 'branch_offices_update.html'
    success_url = reverse_lazy('dentist:branch_offices_list')
    permission_required = 'dentist.change_branchoffices'


class BranchOfficeDelete(PermissionRequiredMixin, DeleteView):
    model = BranchOffices
    success_url = reverse_lazy('dentist:branch_offices_list')
    template_name = 'branch_offices_confirm_delete.html'
    permission_required = 'dentist.delete_branchoffices'


@permission_required(perm='dentist.add_branchoffices', raise_exception=True)
def branch_offices_add(request):
    form = BranchOfficesForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dentist:branch_offices_list')
    return render(request, 'branch_offices_form.html', {'form': form})


def patients_list(request):
    patients = Patients.objects.all()
    return render(request, 'patients_list.html', {'patients': patients})


def patients_add(request):
    form = PatientsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dentist:patients_list')
    return render(request, 'patients_form.html', {'form': form})


def personel_list(request):
    personel = Personel.objects.all()
    return render(request, 'personel_list.html', {'personel': personel})


def user_list(request):
    users = User.objects.all()
    personel = Personel.objects.all()
    return render(request, 'user_list.html', {'users': users, 'personel': personel})


class PersonelAdd(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('dentist:personel_list')
    template_name = 'personel_form.html'

    def get_success_url(self):
        success_url = reverse_lazy('dentist:personel_add_continue', kwargs={'pk': self.object.id})
        return success_url


class PersonelAddContinue(CreateView):
    form_class = PersonelForm
    success_url = reverse_lazy('dentist:personel_list')
    template_name = 'personel_form_continue.html'

    def get_initial(self):
        initial = super().get_initial()
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        initial['user'] = user
        return initial

@receiver(post_save, sender=Personel)
def create_user_group(sender, instance, created, **kwargs):
    if created and instance.role == 'A':
        group, _ = Group.objects.get_or_create(name='Admin')
        instance.user.groups.add(group)
    if created and instance.role == 'D':
        group, _ = Group.objects.get_or_create(name='Dentist')
        instance.user.groups.add(group)
    if created and instance.role == 'R':
        group, _ = Group.objects.get_or_create(name='Receptionist')
        instance.user.groups.add(group)


class PersonelUpdate(PermissionRequiredMixin, UpdateView):
    model = Personel
    form_class = PersonelForm
    template_name = 'personel_update.html'
    success_url = reverse_lazy('dentist:personel_list')
    permission_required = 'dentist.change_personel'


class PersonelDelete(PermissionRequiredMixin, DeleteView):
    model = Personel
    template_name = 'personel_confirm_delete.html'
    success_url = reverse_lazy('dentist:personel_list')
    permission_required = 'dentist.delete_personel'


def visits_list(request):
    visits = Visits.objects.all()
    return render(request, 'visits_list.html', {'visits': visits})


def visits_add(request):
    form = VisitsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dentist:visits_list')
    return render(request, 'visits_form.html', {'form': form})


class VisitDetail(DetailView):
    model = Visits
    template_name = 'visit_detail.html'


class VisitUpdate(PermissionRequiredMixin, UpdateView):
    model = Visits
    form_class = VisitsForm
    template_name = 'visit_update.html'
    success_url = reverse_lazy('dentist:visits_list')
    permission_required = 'dentist.change_visits'


class VisitDelete(PermissionRequiredMixin, DeleteView):
    model = Visits
    template_name = 'visit_confirm_delete.html'
    success_url = reverse_lazy('dentist:visits_list')
    permission_required = 'dentist.delete_visits'


def delete_branch_office(request, pk):
    branch_office = get_object_or_404(BranchOffices, pk=pk)
    if request.method == 'POST':
        branch_office.delete()
        return redirect('dentist:branch_offices_list')
    return render(request, 'delete_branch_office.html', {'branch_office': branch_office})


def EngagementsCal(request):
    branch_offices = BranchOffices.objects.all()
    doctors = Personel.objects.filter(role='D')

    branch_office_filter = request.GET.get('branch_office')
    doctors_filter = request.GET.get('doctors')
    if doctors_filter == "":
        event_arr = getAllVisits(branch_office_filter)
    else:
        event_arr = getAllVisits(branch_office_filter, doctors_filter)

    context = {
        "events": event_arr,
        "doctors": doctors,
        "doctors_filter": doctors_filter,
        "branch_offices": branch_offices,
        "branch_office_filter": branch_office_filter
    }

    return render(request, 'EngagementsCalendar.html', context)


class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('dentist:home')
    template_name = 'registration/change_password.html'


# def password_changes(request):
#     return render(request, 'registration/password_changes.html', {})

