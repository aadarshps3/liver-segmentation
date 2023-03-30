import cv2
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .prediction import model_predict
from .segmentation import segment
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# Create your views here.


################################ display homepage ##############################



def display_home(request):
    return render(request, 'home.html')


################################################################################

################################# display login page ############################

def display_login_page(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('adminpage')
            elif  user.is_doctor:
                return redirect('load_upload_page')
            elif user.is_user:
                return redirect('patientpage')
        else:
            messages.info(request, 'Invalid Credentials')
    return render(request, 'Login.html')


##################################################################################

################################ Load Task Page ###################################

def load_task(request):
    return render(request, 'TASK.html')

def userpage(request):
    return render(request,'userpage.html')

def patientpage(request):
    return render(request,'index.html')

def adminpage(request):
    return render(request,'index1.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        print(username)
        password = request.POST.get('pass')
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('userpage')
            elif  user.is_doctor:
                return redirect('load_upload_page')
            elif user.is_user:
                print('working')
                return redirect('patientpage')
        else:
            messages.info(request, 'Invalid Credentials')
    return render(request, 'Login.html')

def doctor_register(request):
    user_form = LoginRegister()
    doc_form = doctorRegister()
    if request.method == 'POST':
        user_form = LoginRegister(request.POST)
        doc_form = doctorRegister(request.POST, request.FILES)
        if user_form.is_valid() and doc_form.is_valid():
            user = user_form.save(commit=False)
            user.is_doctor = True
            user.save()
            doctor = doc_form.save(commit=False)
            doctor.user = user
            doctor.save()
            messages.info(request, 'Registered Successfully')
            return redirect('display_login_page')
    return render(request, 'doc_reg.html', {'user_form': user_form, 'doc_form': doc_form})


def patient_register(request):
    user_form = LoginRegister()
    pat_form = patientRegister()
    if request.method == 'POST':
        user_form = LoginRegister(request.POST)
        pat_form = patientRegister(request.POST, request.FILES)
        if user_form.is_valid() and pat_form.is_valid():
            user = user_form.save(commit=False)
            user.is_user = True
            user.save()
            patient = pat_form.save(commit=False)
            patient.user = user
            patient.save()
            messages.info(request, 'Registered Successfully')
            return redirect('display_login_page')
    return render(request, 'pat_reg.html', {'user_form': user_form, 'pat_form': pat_form})


##################################################################################

############################## Upload xray ######################################

def load_upload_page(request):
    if request.method == "POST" and 'upload_btn' in request.POST:

        form = upload_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.error(request, "MRI Uploaded Sucessfully!")
        else:
            form = upload_form()
            messages.error(request, "MRI not Uploaded!")

    if request.method == "POST" and 'check_btn' in request.POST:
        obj = upload_img.objects.all().last()
        scr = obj.img_upload
        new_scr = 'media/' + str(scr)
        print("___________the scourse _----------- ")
        print(new_scr)
        get_prediction = model_predict(new_scr)
        print("____________ the prediction ______________")
        print(get_prediction)
        context = {
            "x_ray": obj,
            "prediction": get_prediction
        }
        return render(request, 'choose.html', context)
    if request.method == "POST" and "segment" in request.POST:
        obj = upload_img.objects.all().last()
        scr = obj.img_upload
        new_scr = 'media/' + str(scr)
        print("___________the scourse _----------- ")
        print(new_scr)
        file = new_scr
        image = cv2.imread(file, 1)
        get_prediction = segment(image)
        pil_image = to_image(get_prediction)
        image_uri = to_data_uri(pil_image)
        # result=cv2.imshow(get_prediction)

        # print("____________ the prediction ______________")
        print(get_prediction)
        context = {

            "prediction": image_uri
        }
        return render(request, 'choose1.html', context)

    if request.method == "POST" and 'log_out_btn' in request.POST:
        return redirect('log_out_load')

    return render(request, 'choose.html')


def uploaded_db(request):
    return render(request,'database.html')

###############################################################################

def logout(request):
    return redirect('homepage')


from PIL import Image

def to_image(numpy_img):
    img = Image.fromarray(numpy_img, 'RGB')
    return img
import base64
from io import BytesIO

def to_data_uri(pil_img):
    data = BytesIO()
    pil_img.save(data, "JPEG") # pick your format
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,'+data64.decode('utf-8')

def view_doc_pat(request):
    data = doctor.objects.all()
    return render(request, 'view_doc.html', {'data': data})

def schedule_add_doc(request):
    form = SchdeuleForm()
    if request.method == 'POST':
        form = SchdeuleForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.doctor=doctor.objects.get(user=request.user)
            form.save()
            messages.info(request, 'schedule added successful')
            return redirect('schedule_view')
    return render(request, 'schedule_add.html', {'form': form})


def schedule_view(request):
    u=doctor.objects.get(user=request.user)
    print(u)
    s = Schedule.objects.filter(doctor=u)
    print(s)
    context = {
        'schedule': s
    }
    return render(request, 'schedule_view.html', context)

def view_schedule_patient(request):
    s = Schedule.objects.all()
    context = {
        'schedule': s
    }
    return render(request, 'schedule_view_pat.html', context)


def take_appointment(request, id):
    s = Schedule.objects.get(id=id)
    c = patient.objects.get(user=request.user)
    appointment = Appointment.objects.filter(user=c, schedule=s)
    if appointment.exists():
        messages.info(request, 'You Have Already Requested Appointment for this Schedule')
        return redirect('view_schedule_patient')
    else:
        if request.method == 'POST':
            obj = Appointment()
            obj.user = c
            obj.schedule = s
            obj.save()
            messages.info(request, 'Appointment Booked Successfully')
            return redirect('appointment_view')
    return render(request, 'take_appointment.html', {'schedule': s})

def appointment_view(request):
    c = patient.objects.get(user=request.user)
    a = Appointment.objects.filter(user=c)
    return render(request, 'appointment_view.html', {'appointment': a})

def pat_view_admin(request):
    data=patient.objects.all()
    return render(request,'view_pat_admin.html',{'data':data})

def doc_view_admin(request):
    data=doctor.objects.all()
    return render(request,'view_doc_admin.html',{'data':data})

def appointment_admin(request):
    a = Appointment.objects.all()
    context = {
        'appointment': a,
    }
    return render(request, 'appointmentsad.html', context)


def approve_appointment(request, id):
    a = Appointment.objects.get(id=id)
    a.status = 1
    a.save()
    messages.info(request, 'Appointment  Confirmed')
    return redirect('appointment_admin')



def reject_appointment(request, id):
    n = Appointment.objects.get(id=id)
    n.status = 2
    n.save()
    messages.info(request, 'Appointment Rejected')
    return redirect('appointment_admin')


def logout_view(request):
    logout(request)
    return redirect('display_login_page')
