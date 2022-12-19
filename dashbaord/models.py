from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_slot_time = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)
    day_start_time = models.CharField(max_length=15, null=True)
    day_end_time = models.CharField(max_length=15, null=True)

    def __str__(self):
        return str(self.id) + "_" + self.name


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    patient_email = models.CharField(max_length=100)
    patient_contact = models.CharField(max_length=12)
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=20)
    appointment_status = models.CharField(max_length=10, default="Open")

    def __str__(self):
        return str(self.id) + "_" + self.patient_name


class SummaryReport:
    date: str
    no_appointments: str
    closed_appointments: str
    cancelled_appointments: str


class DetailedReport:
    date: str
    patient_name: str
    status: str
