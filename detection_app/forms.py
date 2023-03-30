from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm




class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'

class upload_form(forms.ModelForm):

    class Meta:
        model=upload_img
        fields=['img_upload']



class LoginRegister(UserCreationForm):
    username=forms.CharField()
    password1=forms.CharField(widget=forms.PasswordInput,label='password')
    password2=forms.CharField(widget=forms.PasswordInput,label='confirm password')

    class Meta:
        model = Login
        fields = ('username', 'password1', 'password2')


class doctorRegister(forms.ModelForm):
    class Meta:
        model = doctor
        exclude=('user',)


class patientRegister(forms.ModelForm):
    class Meta:
        model = patient
        exclude=('user',)

class SchdeuleForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    start_time = forms.TimeField(widget=TimeInput, )
    end_time = forms.TimeField(widget=TimeInput, )

    class Meta:
        model = Schedule
        fields = ( 'date', 'start_time', 'end_time')