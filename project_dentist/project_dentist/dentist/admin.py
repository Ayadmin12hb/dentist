from django.contrib import admin
from .models import BranchOffices, Patients, Personel, Visits


@admin.register(BranchOffices)
class BranchOfficesAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone_number']


@admin.register(Patients)
class PatientsAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'phone_number', 'email', 'pesel']


@admin.register(Personel)
class PersonelAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'role']


@admin.register(Visits)
class VisitsAdmin(admin.ModelAdmin):
    list_display = ['date', 'patient', 'doctor', 'branch_office', 'price', 'service', 'visit_duration']
