"""detection_pjct URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .import views


urlpatterns = [
    ########################## Homepage url #####################
    path('', views.display_home,name="homepage"),
    ########################## Login page url ####################
    path('display_login_page',views.display_login_page,name="display_login_page"),
    ########################## Task page Url ######################
    path("display_task_page",views.load_task,name="task_load"),
    ######################### Upload xray #######################
    path("load_upload_page",views.load_upload_page,name="load_upload_page"),
    ######################### Uploaded  images view #######################
    path('uploaded_db',views.uploaded_db,name='uploaded_db'),
    ######################## Log out Url #########################
    path("log_out_page",views.logout,name="log_out_load"),
    path("logout_view",views.logout_view,name="logout_view"),
    path("userpage",views.userpage,name="userpage"),
    path("doctor_register",views.doctor_register,name="doctor_register"),
    path("login_view",views.login_view,name="login_view"),
    path("patient_register",views.patient_register,name="patient_register"),
    path("patientpage",views.patientpage,name="patientpage"),
    path("adminpage",views.adminpage,name="adminpage"),
    path("view_doc_pat",views.view_doc_pat,name="view_doc_pat"),
    path("schedule_add_doc",views.schedule_add_doc,name="schedule_add_doc"),
    path("schedule_view",views.schedule_view,name="schedule_view"),
    path("view_schedule_patient",views.view_schedule_patient,name="view_schedule_patient"),
    path("take_appointment/<int:id>/",views.take_appointment,name="take_appointment"),
    path("approve_appointment/<int:id>/",views.approve_appointment,name="approve_appointment"),
    path("reject_appointment/<int:id>/",views.reject_appointment,name="reject_appointment"),
    path("appointment_view",views.appointment_view,name="appointment_view"),
    path("pat_view_admin",views.pat_view_admin,name="pat_view_admin"),
    path("doc_view_admin",views.doc_view_admin,name="doc_view_admin"),
    path("appointment_admin",views.appointment_admin,name="appointment_admin"),
]
