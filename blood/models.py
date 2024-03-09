from django.db import models
from datetime import datetime ,timedelta,date
from patient import models as pmodels
from donor import models as dmodels
class Stock(models.Model):
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    expire_date=models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return self.bloodgroup

class BloodRequest(models.Model):
    request_by_patient=models.ForeignKey(pmodels.Patient,null=True,on_delete=models.CASCADE)
    request_by_donor=models.ForeignKey(dmodels.Donor,null=True,on_delete=models.CASCADE)
    patient_name=models.CharField(max_length=30)
    patient_age=models.PositiveIntegerField()
    reason=models.CharField(max_length=500)
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    rbc = models.CharField(max_length=40)
    wbc = models.CharField(max_length=40)
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now=True)
    # expire_date=models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return self.bloodgroup
    
    # @property
    # def get_name(self):
    #     return self.user.first_name+" "+self.user.last_name
    
    # @property
    # def get_instance(self):
    #     return self
    # def __str__(self):
    #     return self.user.first_name

    
    
class contact(models.Model):
    first_name=models.CharField(max_length=40)
    last_name= models.CharField(max_length=40)

    age=models.PositiveIntegerField()
    bloodgroup=models.CharField(max_length=10)
    disease=models.CharField(max_length=100)
    doctorname=models.CharField(max_length=50)

    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

        