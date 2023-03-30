from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Login(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

class doctor(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='worker')
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    experience = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class patient(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='patient')
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class upload_img(models.Model):
    img_upload=models.ImageField(upload_to='uploads')

class Schedule(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

class Appointment(models.Model):
    user = models.ForeignKey(patient, on_delete=models.CASCADE, related_name='appointment')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)


