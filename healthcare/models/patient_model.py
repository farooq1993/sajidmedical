from django.db import models
from django.core.validators import RegexValidator
from datetime import timedelta, datetime
from django.utils import timezone
import random

class AppointmentMaster(models.Model):
    patient = models.ForeignKey("healthcare.UserMaster", related_name='patient_appointment', null=True,
                on_delete=models.CASCADE)
    doctor = models.ForeignKey("healthcare.UserMaster", related_name='doctor_appointment', null=True,
                on_delete=models.CASCADE)
    patient_family = models.ForeignKey("healthcare.UserMaster", related_name='patient_fmaily_appointment', null=True,
                on_delete=models.CASCADE)
    appointment_type = models.CharField(max_length=300,default=None,null=True)
    appointment_code = models.CharField(max_length=300,default=None,null=True)
    other_symptoms = models.TextField(null=True)
    date = models.DateField(null=True)
    time_slot_from = models.TimeField(null=True)
    time_slot_to = models.TimeField(null=True)
    added_by = models.ForeignKey("healthcare.UserMaster",related_name='appointment_added_by',on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey("healthcare.UserMaster",related_name='appointment_updated_by',on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.appointment_code:
            number = (datetime.today().strftime('%B'),f'#{datetime.today().year}',f'#{random.randint(1000,999999)}')
            appointment_code = "".join(number)
            self.appointment_code = appointment_code
        return super(AppointmentMaster, self).save(*args, **kwargs)
    class Meta:
        db_table = 'appointment_master'

class AppointmentDetails(models.Model):
    appointment = models.ForeignKey("healthcare.AppointmentMaster", related_name='appointment_details', null=True,
                on_delete=models.CASCADE)
    symptom = models.ForeignKey("healthcare.SymptomDetails",related_name='symptom_master',on_delete=models.CASCADE, null=True)
    added_by = models.ForeignKey("healthcare.UserMaster",related_name='appointment_detail_added_by',on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey("healthcare.UserMaster",related_name='appointment_detail_updated_by',on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'appointment_details'

class PatientFamilyDetails(models.Model):
    patient = models.ForeignKey("healthcare.UserMaster", related_name='patient_family', null=True,
                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=130,default=None,null=True)
    last_name = models.CharField(max_length=130,default=None,null=True)
    full_name = models.CharField(max_length=130,default=None,null=True)
    mobile_number = models.CharField(max_length=15,default=None,null=True)
    address_1 = models.CharField(max_length=200, default=None, null=True)
    address_2 = models.CharField(max_length=200, default=None, null=True)
    city = models.CharField(max_length=200, default=None, null=True)
    state = models.CharField(max_length=200, default=None, null=True)
    pincode = models.CharField(max_length=20, default=None, null=True)
    age = models.IntegerField(null=True)
    dob = models.DateField(null=True)
    country = models.CharField(max_length=200, default=None, null=True)
    gender = models.CharField(max_length=200, default=None, null=True)
    qualification = models.CharField(max_length=200, default=None, null=True)
    occupation = models.CharField(max_length=300, default=None, null=True)
    email_id = models.CharField(max_length=500, null=True)
    medical_history = models.TextField()
    is_active = models.BooleanField(default=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'patient_family_member'