from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.contrib import messages
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from donor import models as dmodels
from patient import models as pmodels
import datetime,time,pymongo
from donor import forms as dforms
from patient import forms as pforms
from django.contrib import messages

def home_view(request):
    x=models.Stock.objects.all()
    print(x)
    if len(x)==0:
        blood1=models.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=models.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=models.Stock()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=models.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=models.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=models.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=models.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=models.Stock()
        blood8.bloodgroup="O-"
        blood8.save()

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'blood/index.html')

def is_donor(user):
    return user.groups.filter(name='DONOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def contact_view(request):
    patient= models.contact.objects.all()
    context = {'Patient':patient}
    return render(request,'blood/contact.html',context)

def afterlogin_view1(request):
    username= request.POST['username']
    password= request.POST['password']
    user = user.is_authenticated(username=username, password=password)
    if user is not None:
        if user.is_active:
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
            messages.success(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect('adminlogin',messages)
        return render(request,'blood/adminlogin',context=messages)

            # Redirect to a success page.
            
    
@login_required(login_url='adminlogin')
def afterlogin_view1(request):
    form=forms.form()
    mydict={'form':form}
    if request.method=='POST':
        form=forms.form(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            messages.success(request, 'Your profile is updated successfully!')
        return HttpResponseRedirect('admin-dashboard')
    return render(request,'blood/admin-dashboardhtml',context=mydict)
    # donor_blood_expiry_date = 11
    # datetime_object = datetime.datetime.strptime(datetime.datetime.today().strftime("%d/%m/%Y"), '%d/%m/%Y')
    # donations=dmodels.BloodDonate.objects.all().filter(expire_date = datetime_object+datetime.timedelta(days=donor_blood_expiry_date)).count()
    # messages.success(request, 'Your profile is updated successfully!')
    # return redirect('admin-dashboard',{'donations':donations})
    


def afterlogin_view(request):
    if is_donor(request.user):      
        return redirect('donor/donor-dashboard')
                
    elif is_patient(request.user):
        return redirect('patient/patient-dashboard')
    else:
        client = pymongo.MongoClient("mongodb+srv://testuser750:mongoDb_750@ehrblock.nvomfgg.mongodb.net/?retryWrites=true&w=majority")
        db = client.testuser750
        mydb=client['bloodbank']
        myrow=mydb['donor_blooddonate']
        # cursor = myrow.find().sort([('timestamp', -1)]).limit(1)
        #donor_blood_expiry_date = 11
        #datetime_object = datetime.datetime.strptime(datetime.datetime.today().strftime("%d/%m/%Y"), '%d/%m/%Y')
        #donations=dmodels.BloodDonate.objects.all().filter(expire_date= datetime_object+datetime.timedelta(days=donor_blood_expiry_date)).count()
        donor_blood_expiry_date = 10
        datetime_object = datetime.datetime.strptime(datetime.datetime.today().strftime("%d/%m/%Y"), '%d/%m/%Y')
        start_date = date.today()
        end_date = start_date + timedelta(days=donor_blood_expiry_date)
        donations=dmodels.BloodDonate.objects.filter(expire_date__range=(start_date, end_date)).count()
    
        plasma='Batch is ready for plasma creation'
        #donations=dmodels.BloodDonate.objects.all().filter().count()
        donations1= str(donations)  +  plasma
        messages.success(request, donations1)
        return redirect('admin-dashboard')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    totalunit=models.Stock.objects.aggregate(Sum('unit'))
    dict={

        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
        'totaldonors':dmodels.Donor.objects.all().count(),
        'totalbloodunit':totalunit['unit__sum'],
        'totalrequest':models.BloodRequest.objects.all().count(),
        'totalapprovedrequest':models.BloodRequest.objects.all().filter(status='Approved').count()
    }
    return render(request,'blood/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_blood_view(request):
    dict={
        'bloodForm':forms.BloodForm(),
        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
    }
    if request.method=='POST':
        bloodForm=forms.BloodForm(request.POST)
        if bloodForm.is_valid() :        
            bloodgroup=bloodForm.cleaned_data['bloodgroup']
            stock=models.Stock.objects.get(bloodgroup=bloodgroup)
            stock.unit=bloodForm.cleaned_data['unit']
            stock.save()
        return HttpResponseRedirect('admin-blood')
    return render(request,'blood/admin_blood.html',context=dict)


@login_required(login_url='adminlogin')
def admin_donor_view(request):
    donors=dmodels.Donor.objects.all()
    return render(request,'blood/admin_donor.html',{'donors':donors})

@login_required(login_url='adminlogin')
def update_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=dmodels.User.objects.get(id=donor.user_id)
    userForm=dforms.DonorUserForm(instance=user)
    donorForm=dforms.DonorForm(request.FILES,instance=donor)
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=dforms.DonorUserForm(request.POST,instance=user)
        donorForm=dforms.DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            return redirect('admin-donor')
    return render(request,'blood/update_donor.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    return HttpResponseRedirect('/admin-donor')

@login_required(login_url='adminlogin')
def admin_patient_view(request):
    patients=pmodels.Patient.objects.all()
    return render(request,'blood/admin_patient.html',{'patients':patients})


@login_required(login_url='adminlogin')
def update_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=pmodels.User.objects.get(id=patient.user_id)
    userForm=pforms.PatientUserForm(instance=user)
    patientForm=pforms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=pforms.PatientUserForm(request.POST,instance=user)
        patientForm=pforms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            return redirect('admin-patient')
    return render(request,'blood/update_patient.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return HttpResponseRedirect('/admin-patient')

@login_required(login_url='adminlogin')
def admin_request_view(request):
    requests=models.BloodRequest.objects.all().filter(status='Pending')
    return render(request,'blood/admin_request.html',{'requests':requests})

@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests=models.BloodRequest.objects.all().exclude(status='Pending')
    return render(request,'blood/admin_request_history.html',{'requests':requests})

@login_required(login_url='adminlogin')
def admin_donation_view(request):
    donations=dmodels.BloodDonate.objects.all()
    return render(request,'blood/admin_donation.html',{'donations':donations})

@login_required(login_url='adminlogin')
def update_approve_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    message=None
    bloodgroup=req.bloodgroup
    unit=req.unit
    stock=models.Stock.objects.get(bloodgroup=bloodgroup)
    if stock.unit > unit:
        stock.unit=stock.unit-unit
        stock.save()
        req.status="Approved"
        
    else:
        message="Stock Doest Not Have Enough Blood To Approve This Request, Only "+str(stock.unit)+" Unit Available"
    req.save()

    requests=models.BloodRequest.objects.all().filter(status='Pending')
    return render(request,'blood/admin_request.html',{'requests':requests,'message':message})

@login_required(login_url='adminlogin')
def update_reject_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    req.status="Rejected"
    req.save()
    return HttpResponseRedirect('/admin-request')

@login_required(login_url='adminlogin')
def approve_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation_blood_group=donation.bloodgroup
    donation_blood_unit=donation.unit

    stock=models.Stock.objects.get(bloodgroup=donation_blood_group)
    stock.unit=stock.unit+donation_blood_unit
    stock.save()

    donation.status='Approved'
    donation.save()
    return HttpResponseRedirect('/admin-donation')

# @login_required(login_url='adminlogin')
# def expiretable_view(request,pk):
#     donation=dmodels.BloodDonate.objects.get(id=pk)
#     donation_blood_group=donation.bloodgroup
#     donation_blood_unit=donation.unit

#     stock=models.Stock.objects.get(bloodgroup=donation_blood_group)
#     stock.unit=stock.unit+donation_blood_unit
#     stock.save()

#     donation.status='Approved'
#     donation.save()
#     return HttpResponseRedirect('/expiretable')

@login_required(login_url='adminlogin')
def expiretable_view(request):
    donor_blood_expiry_date = 15
    # donor_blood_expiry_date2 = 30
    datetime_object = datetime.datetime.strptime(datetime.datetime.today().strftime("%d/%m/%Y"), '%d/%m/%Y')
    start_date = date.today()
    end_date = start_date + timedelta(days=donor_blood_expiry_date)
    donations=dmodels.BloodDonate.objects.filter(expire_date__range=(start_date, end_date))
    #+ timedelta(days=expiry_date)datetime.datetime(2023, 3, 24, 1, 10, 15,888000))
    # today = date.today()
    # week = today - timedelta(days=7)
    # donations = dmodels.BloodDonate.objects.filter(date=week).filter(expire_date=False)
    # return len(donations)
    # donations=dmodels.BloodDonate.objects.all() 
    # # donor= models.Donor.objects.get(user_id=request.user.id)
    client = pymongo.MongoClient("mongodb+srv://testuser750:mongoDb_750@ehrblock.nvomfgg.mongodb.net/?retryWrites=true&w=majority")
    db = client.testuser750
    mydb=client['bloodbank']
    myrow=mydb['donor_blooddonate']
    # # cursor = myrow.find({'expire_date': 20 })
    # #mylist=myrow.find_one()
    # # mylist=myrow.find_one({ "expire_date": {moment().subtract(7, 'days').toDate() } }) 
    cursor = myrow.find()
    print("================")
    for each_mylist in cursor:
        print('mylist')
        print(each_mylist)
    
    return render(request,'blood/expiretable.html',{'donations':donations})



@login_required(login_url='adminlogin')
def reject_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation.status='Rejected'
    donation.save()
    return HttpResponseRedirect('/admin-donation')