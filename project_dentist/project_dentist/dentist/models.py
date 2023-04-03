from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime


class BranchOffices(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=1024)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.name}, {self.address}"


class Patients(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    pesel = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Personel(models.Model):
    ROLE = {
        ('A', 'Admin'),
        ('R', 'Receptionist'),
        ('D', 'Dentist'),
    }
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    role = models.CharField(max_length=128, choices=ROLE)
    # branch_office = models.ForeignKey(BranchOffices, on_delete=models.CASCADE, default=None, null=True)
    branch_office = models.ManyToManyField(BranchOffices, default=None, null=True, blank=True)
    start_work = models.TimeField(default="08:00:00")
    end_work = models.TimeField(default="16:00:00")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Visits(models.Model):
    date = models.DateTimeField()
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Personel, on_delete=models.CASCADE, limit_choices_to={'role': 'D'})
    branch_office = models.ForeignKey(BranchOffices, on_delete=models.CASCADE)
    price = models.IntegerField()
    service = models.CharField(max_length=512)
    visit_duration = models.TimeField(default=datetime.time(0, 10))


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


def getAllVisits(branch_office=None, doctor=None):
    event_arr = []
    if branch_office:
        if doctor:
            all_visits = Visits.objects.filter(doctor__user__id=doctor, branch_office__id=branch_office)
        else:
            all_visits = Visits.objects.filter(branch_office__id=branch_office)
    elif doctor:
        all_visits = Visits.objects.filter(doctor__user__id=doctor)
    else:
        all_visits = Visits.objects.all()

    colors = ["#990000", "#994C00", "#666600",
              "#336600", "#006600", "#006633",
              "#006666", "#003366", "#000066",
              "#330066", "#660066", "#660033",
              "#202020"]

    for visit in all_visits:
        event_sub_arr = {}
        event_sub_arr['title'] = f" | service: {str(visit.service)} | patient: {(str(visit.patient))}"
        start_time = visit.date.strftime("%Y-%m-%dT%H:%M:%S")
        end_time = (visit.date + datetime.timedelta(hours=visit.visit_duration.hour,
                                                    minutes=visit.visit_duration.minute)).strftime("%Y-%m-%dT%H:%M:%S")
        event_sub_arr['start'] = start_time
        event_sub_arr['end'] = end_time
        event_sub_arr['id'] = visit.id
        event_sub_arr['color'] = colors[visit.id % len(colors)]
        event_arr.append(event_sub_arr)
    return event_arr
