from django.shortcuts import render,redirect
from . import forms,models
from django.shortcuts import render
import requests
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.http import HttpResponse 
from datetime import date, timedelta
import datetime,time,pymongo
from hashlib import sha256
import json
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels

import time
from datetime import datetime ,timedelta,date

def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patcreate')
    return render(request,'patient/patientsignup.html',context=mydict)
               

    

def patient_dashboard_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count(),

    }
   
    return render(request,'patient/patient_dashboard.html',context=dict)

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            patient= models.Patient.objects.get(user_id=request.user.id)
            blood_request.request_by_patient=patient
            if blood_request.bloodgroup == "O+":
                expiry_date = 10
            elif blood_request.bloodgroup == "O+":
                expiry_date = 15
            elif blood_request.bloodgroup == "O-":
                expiry_date = 20
            elif blood_request.bloodgroup == "AB+":
                expiry_date = 25
            elif blood_request.bloodgroup == "AB-":
                expiry_date = 30
            elif blood_request.bloodgroup == "A+":
                expiry_date = 35
            elif blood_request.bloodgroup == "A-":
                expiry_date = 40
            elif blood_request.bloodgroup == "B+":
                expiry_date = 45
            elif blood_request.bloodgroup == "B-":
                expiry_date = 50
            
            blood_request.expire_date = (datetime.today() + timedelta(days=expiry_date))
            blood_request.save()
            return HttpResponseRedirect('my-request')
    
    return render(request,'patient/makerequest.html',{'request_form':request_form})

def my_request_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient)
    return render(request,'patient/my_request.html',{'blood_request':blood_request})


def patcreate_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    userForm=forms.PatientUserForm(request.POST)
    patient= models.Patient.objects.all()
    User1= models.User.objects.all()
    context = {'Patient':patient,'User':User1}
    return render(request, 'patient/patcreate.html', context)




# def patcreate_view(request):
#     # patient= models.Patient.objects.get(user_id=request.user.id)
#     userForm=forms.PatientUserForm()
#     patientForm=forms.PatientForm()
#     mydict={'userForm':userForm,'patientForm':patientForm}
#     # first_name=request.form['first_name']
#     # last_name=request.form['last_name']
#     # username=request.form['username']
#     # password= request.form['password']
#     # password=request.form(password)
#     age=models.Patient.objects.get['age']
#     bloodgroup=models.Patient.objects.get['bloodgroup']
#     disease=models.Patient.objects.get['disease']
#     doctorname=models.Patient.objects.get['doctornam']
#     address=models.Patient.objects.get['address']
#     mobile=models.Patient.objects.get['mobile']
#     # profile_pic=request.form['profile_pic']
#     client = pymongo.MongoClient("mongodb+srv://testuser750:mongoDb_750@ehrblock.nvomfgg.mongodb.net/?retryWrites=true&w=majority")
#     db = client.testuser750
#     mydb=client['bloodbank']
#     myrow=mydb['patient_patient']
#     patdoc= myrow.find()
#     ind=-1
#     for x in patdoc:
#         prev=x['hash']
#         ind=ind+1

#     i='PAT00'+str(ind+1)
#     block={
#     'user_id':i,
#     # 'first_name':first_name,
#     # 'last_name': last_name,
#     # 'username':username,
#     # 'password': password,
#     'age':age,
#     'bloodgroup':bloodgroup,
#     'disease':disease,
#     'doctorname':doctorname,
#     'address':address,
#     'mobile':mobile,
#     # 'profile_pic':profile_pic,
#     'prevhash':"prev"
# }
#     block_string = json.dumps(block, sort_keys=True)
#     print('block_string:::',block_string)
#     hashval=sha256(block_string.encode()).hexdigest()
#     request.session['user']=i
#     block={
#     'user_id':i,
#     # 'first_name':first_name,
#     # 'last_name': last_name,
#     # 'username':username,
#     # 'password': password,
#     'age':age,
#     'bloodgroup':bloodgroup,
#     'disease':disease,
#     'doctorname':doctorname,
#     'address':address,
#     'mobile':mobile,
#     # 'profile_pic':profile_pic,
#     'prevhash':prev,
#     'hash': hashval
# }
#     myrow.insert_one(block)
    
    
#     Blockc=[]
#     Bloc=myrow.find()
#     for i in Bloc:
#         Blockc.append(i)
#     return render(request,'patient/patcreate.html',Patient=Blockc)

  
