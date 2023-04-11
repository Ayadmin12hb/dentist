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
    first_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'style': 'max-width: 20%;'}))
    last_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'style': 'max-width: 20%;'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'style': 'max-width: 20%;'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['style'] = 'max-width: 20%'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['style'] = 'max-width: 20%'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['style'] = 'max-width: 20%'


class PersonelForm(forms.ModelForm):
    class Meta:
        model = Personel
        fields = ('user', 'phone_number', 'role', 'branch_office', 'start_work', 'end_work')
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'style': 'max-width: 10%;',
                                                     'type': 'number'}),
            'role': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 10%; text-align: center',
                                        'type': 'select'}),
            'branch_office': forms.CheckboxSelectMultiple(attrs={'type': 'checkbox'}),
            'start_work': forms.TimeInput(attrs={'class': 'form-control', 'style': 'max-width: 10%;', 'type': 'time'}),
            'end_work': forms.TimeInput(attrs={'class': 'form-control', 'style': 'max-width: 10%;', 'type': 'time'}),
        }


class VisitsForm(forms.ModelForm):
    class Meta:
        model = Visits
        fields = ['date', 'patient', 'doctor', 'branch_office', 'price', 'service', 'visit_duration']
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'style': 'max-width: 15%;',
                                               'type': 'datetime-local'}),
            'patient': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 15%;',
                                           'type': 'select'}),
            'doctor': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 15%;',
                                          'type': 'select'}),
            'branch_office': forms.Select(attrs={'class': 'form-control',
                                                 'style': 'max-width: 15%;', 'type': 'select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'style': 'max-width: 10%;', 'type': 'number'}),
            'service': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 30%; max-height: 100px;',
                                             'type': 'text'}),
            'visit_duration': forms.TimeInput(attrs={'class': 'form-control', 'style': 'max-width: 8%;',
                                                     'type': 'time'})
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        doctor = cleaned_data.get('doctor')
        visit_duration = cleaned_data.get('visit_duration')

        if date and doctor and visit_duration:
            hours, minutes = visit_duration.hour, visit_duration.minute
            visit_timedelta = datetime.timedelta(hours=hours, minutes=minutes)

            start_time = datetime.datetime.combine(date.date(), date.time())
            end_time = start_time + visit_timedelta

            existing_visits = Visits.objects.filter(doctor=doctor, date__date=date.date()).exclude(date=date)

            if doctor.start_work > start_time.time():
                raise forms.ValidationError("The doctor has not started work yet")
            if doctor.end_work < end_time.time():
                raise forms.ValidationError("The doctor already finished work")

            for visit in existing_visits:

                visit_start_time = datetime.datetime.combine(visit.date.date(), visit.date.time())
                hours, minutes = visit.visit_duration.hour, visit.visit_duration.minute
                visit_timedelta = datetime.timedelta(hours=hours, minutes=minutes)
                visit_end_time = visit_start_time + visit_timedelta

                if visit_start_time < start_time < visit_end_time:
                    raise forms.ValidationError('This doctor already has an appointment at this time')
                if visit_end_time > end_time > visit_start_time:
                    raise forms.ValidationError('This doctor already has an appointment at this time')
                if visit_start_time > start_time and visit_end_time < end_time:
                    raise forms.ValidationError('This doctor already has an appointment at this time')

            return cleaned_data


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password',
                                          'style': 'max-width: 20%;'}))
    new_password1 = forms.CharField(
        max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password',
                                                         'style': 'max-width: 20%;'}))
    new_password2 = forms.CharField(
        max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password',
                                                         'style': 'max-width: 20%;'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
