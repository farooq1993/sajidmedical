from django.db import models
from django.contrib.auth.models import User
from healthcare.utils import constants
from django.contrib.postgres.fields import ArrayField

class MedicineMaster(models.Model):
    medicine_name = models.CharField(max_length=300,default=None,null=True)
    medicine_type = models.CharField(max_length=300,default=None,null=True)
    cost_of_medicine = models.DecimalField(decimal_places=2, max_digits=50, blank=True, null=True)
    purpose = models.CharField(max_length=300,default=None,null=True)
    medicine_desc = models.TextField(null=True)
    manufacturer = models.CharField(max_length=130,default=None,null=True)
    acronym = models.CharField(max_length=500, null=True)
    added_by = models.ForeignKey("healthcare.UserMaster",related_name='medicine_added_by',on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey("healthcare.UserMaster",related_name='medicine_updated_by',on_delete=models.CASCADE, null=True)
    verified_by = models.ForeignKey("healthcare.UserMaster",related_name='medicine_verified',on_delete=models.CASCADE, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)
    strength = models.CharField(max_length=128,default=None,null=True)
    drug = models.CharField(max_length=200,default=None,null=True)

    class Meta:
        db_table = "medicine_master"

class Prescription(models.Model):
    doctor = models.ForeignKey("healthcare.UserMaster",related_name='prescription_doctor',on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey("healthcare.UserMaster",related_name='prescription_patient',on_delete=models.CASCADE, null=True)
    medicine_recomended_from_inside = models.ForeignKey("healthcare.MedicineMaster",related_name='medicine_recomended',on_delete=models.CASCADE, null=True)
    medicine_recomended_from_outside = models.CharField(max_length=300,default=None,null=True)
    next_consult = models.CharField(max_length=300,default=None,null=True)
    advoice_list = ArrayField(models.CharField(max_length=300), blank=True, null=True)
    symptom_details = models.TextField(null=True)
    pdf_path = models.CharField(max_length=500, default=None, null=True)
    visiting_fees = models.CharField(max_length=128,default=None,null=True)
    added_by = models.ForeignKey("healthcare.UserMaster",related_name='created_prescription',on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey("healthcare.UserMaster",related_name='updated_prescription',on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "prescription"

class TestMaster(models.Model):
    name = models.CharField(max_length=128,null=True,blank=True)
    body_part = models.CharField(max_length=128,null=True,blank=True)
    test_type = models.CharField(max_length=128,null=True,blank=True)
    desc = models.TextField(null=True)
    added_by = models.ForeignKey("healthcare.UserMaster",related_name='test_added_by',on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey("healthcare.UserMaster",related_name='test_updated_by',on_delete=models.CASCADE, null=True)
    verified_by = models.ForeignKey("healthcare.UserMaster",related_name='test_verified',on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = "test_master"

class PrescriptionMedicineDetails(models.Model):
    prescription = models.ForeignKey("healthcare.Prescription", related_name='precription_medicine_level',on_delete=models.CASCADE, null=True,blank=True)
    medicine = models.ForeignKey("healthcare.MedicineMaster",related_name='precription_medicine',on_delete=models.CASCADE, null=True,blank=True)
    regime = models.CharField(max_length=128,default=None,null=True,blank=True)
    tenure = models.CharField(max_length=128,default=None,null=True,blank=True)
    instruction = models.CharField(max_length=300,default=None,null=True,blank=True)
    added_by = models.ForeignKey("healthcare.UserMaster",related_name='add_pres_medcn_details',on_delete=models.CASCADE, null=True,blank=True)
    updated_by = models.ForeignKey("healthcare.UserMaster",related_name='updated_pres_medcn_details',on_delete=models.CASCADE, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "prescription_medicine_details"

class PrescriptionTestDetails(models.Model):
    prescription = models.ForeignKey("healthcare.Prescription", related_name='precription_test_level',on_delete=models.CASCADE, null=True,blank=True)
    test = models.ForeignKey("healthcare.TestMaster",related_name='precription_test',on_delete=models.CASCADE, null=True,blank=True)
    details = models.TextField(null=True,default=None,blank=True)
    added_by = models.ForeignKey("healthcare.UserMaster",related_name='add_presc_test_details',on_delete=models.CASCADE, null=True,blank=True)
    updated_by = models.ForeignKey("healthcare.UserMaster",related_name='updated_presc_test_details',on_delete=models.CASCADE, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = "prescription_test_details"