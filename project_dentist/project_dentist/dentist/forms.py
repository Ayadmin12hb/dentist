import datetime

from django import forms
from .models import BranchOffices, Patients, Personel, Visits
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class BranchOfficesForm(forms.ModelForm):
    class Meta:
        model = BranchOffices
        fields = '__all__'


class PatientsForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = '__all__'


class UserForm(UserCreationForm):

    username = forms.CharField(max_length=64)
    first_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class PersonelForm(forms.ModelForm):
    class Meta:
        model = Personel
        fields = ('user', 'phone_number', 'role', 'branch_office', 'start_work', 'end_work')
        widgets = {
            'role': forms.RadioSelect(),
            'user': forms.HiddenInput(),
            'branch_office': forms.CheckboxSelectMultiple()
        }


class VisitsForm(forms.ModelForm):
    class Meta:
        model = Visits
        fields = ['date', 'patient', 'doctor', 'branch_office', 'price', 'service', 'visit_duration']
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'patient': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'doctor': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'branch_office': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'service': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'visit_duration': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        doctor = cleaned_data.get('doctor')
        visit_duration = cleaned_data.get('visit_duration')

        if date and doctor:
            hours, minutes = visit_duration.hour, visit_duration.minute
            visit_timedelta = datetime.timedelta(hours=hours, minutes=minutes)

            start_time = datetime.datetime.combine(date.date(), date.time())
            end_time = start_time + visit_timedelta

            existing_visits = Visits.objects.filter(doctor=doctor, date__date=date.date())
            print(existing_visits)

            for visit in existing_visits:

                visit_start_time = datetime.datetime.combine(visit.date.date(), visit.date.time())
                hours, minutes = visit.visit_duration.hour, visit.visit_duration.minute
                visit_timedelta = datetime.timedelta(hours=hours, minutes=minutes)
                visit_end_time = visit_start_time + visit_timedelta

                if visit_start_time < start_time and visit_end_time > start_time:
                    raise forms.ValidationError('This doctor already has an appointment at this time')
                elif visit_end_time > end_time and visit_start_time < end_time:
                    raise forms.ValidationError('This doctor already has an appointment at this time')
                elif visit_start_time > start_time and visit_end_time < end_time:
                    raise forms.ValidationError('This doctor already has an appointment at this time')

            return cleaned_data


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(
        max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(
        max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
