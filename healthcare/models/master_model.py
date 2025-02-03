from django.db import models
from django.core.validators import RegexValidator
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission,BaseUserManager

class CustomUserManager(BaseUserManager):
    """Manager for custom user model to handle email or username login."""
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
    

class OTPGenerator(models.Model):
    """
    Base Class for storing OTP generated as
    a part of validating mobile number
    """
    otp_number = models.IntegerField()
    expired_at = models.DateTimeField(null=True)
    mobile_number = models.CharField(max_length=15,null=True)
    email_id = models.CharField(max_length=500,null=True)
    created_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'otp_generator'


class UserType(models.Model):
    user_type_name = models.CharField(max_length=130,default=None,null=True)
    is_active = models.BooleanField(default=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'user_type'

class User(AbstractUser):
    DOCTOR = 'doctor'
    PATIENT = 'patient'
    
    USER_TYPE_CHOICES = [
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
    ]

    user_name = models.CharField(max_length=130, default=None, null=True)
    first_name = models.CharField(max_length=130, default=None, null=True)
    last_name = models.CharField(max_length=130, default=None, null=True)
    full_name = models.CharField(max_length=130, default=None, null=True)
    mobile_number = models.CharField(max_length=15, default=None, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)
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
    experience = models.CharField(max_length=200, default=None, null=True)
    currently_working_at = models.CharField(max_length=200, default=None, null=True)
    speciality = models.CharField(max_length=300, default=None, null=True)
    occupation = models.CharField(max_length=300, default=None, null=True)
    #verified_by = models.ForeignKey(to='self', related_name='verified_by_admin_user', on_delete=models.SET_NULL, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_id = models.CharField(max_length=500, null=True)
    #doctor = models.ForeignKey(to='self', related_name='user_master_doctor', on_delete=models.CASCADE, null=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

    groups = models.ManyToManyField(Group, related_name="healthcare_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="healthcare_user_permissions", blank=True)

    def __str__(self):
        return self.user_type

    
class UserMaster(models.Model):
    DOCTOR = 'doctor'
    PATIENT = 'patient'
    
    USER_TYPE_CHOICES = [
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
    ]
    user_name = models.CharField(max_length=130,default=None,null=True)
    first_name = models.CharField(max_length=130,default=None,null=True)
    last_name = models.CharField(max_length=130,default=None,null=True)
    full_name = models.CharField(max_length=130,default=None,null=True)
    mobile_number = models.CharField(max_length=15,default=None,null=True)
    # user_type = models.ForeignKey("healthcare.UserType", related_name='user_master_user_type', null=True,
    #             blank=True,on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10,choices=USER_TYPE_CHOICES,null=True,blank=True)
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
    experience = models.CharField(max_length=200, default=None, null=True)
    currently_working_at = models.CharField(max_length=200, default=None, null=True)
    speciality = models.CharField(max_length=300, default=None, null=True)
    occupation = models.CharField(max_length=300, default=None, null=True)
    verified_by = models.ForeignKey(to='self',related_name='verified_by_admin_user', on_delete=models.SET_NULL, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_id = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(User, related_name='auth_user',  on_delete=models.SET_NULL,null=True)
    doctor = models.ForeignKey(to='self', related_name='user_master_doctor', on_delete=models.CASCADE,null=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'user_master'

class PasswordMaster(models.Model):
    user_master = models.ForeignKey("healthcare.UserMaster",related_name='user_master_password',on_delete=models.CASCADE, null=True)
    user = user = models.ForeignKey(User, related_name='user_password', on_delete=models.CASCADE,null=True)
    password = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'password_master'

class CronScriptLock(models.Model):
    RUNNING, STOPPED = (
        "running", "stopped")
    cron_script_name = models.CharField(max_length=128)
    is_one_time_cron = models.BooleanField(default=False)
    one_time_cron_status = models.CharField(max_length=128)
    one_time_cron_started_dt = models.DateTimeField(default=timezone.now)
    one_time_cron_ended_dt = models.DateTimeField(default=timezone.now)
    regular_cron_status = models.CharField(max_length=128)
    regular_cron_started_dt = models.DateTimeField(default=timezone.now)
    regular_cron_ended_dt = models.DateTimeField(default=timezone.now)
    flag_date = models.DateTimeField(null=True)
    data_from_date = models.DateTimeField(null=True)
    created_by = models.ForeignKey('healthcare.UserMaster', related_name="cronscriptlock_created_by_user",
                                   null=True, blank=True, on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cron_script_lock'


class SymptomMaster(models.Model):
    body_part_name = models.CharField(max_length=300, blank=True,null=True)
    added_by = models.ForeignKey("healthcare.UserMaster",related_name='symptoms_added_by',on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey("healthcare.UserMaster",related_name='symptoms_updated_by',on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "symptom_master"

class SymptomDetails(models.Model):
    symptoms = models.ForeignKey("healthcare.SymptomMaster",related_name='symptoms_master_details',on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=300, blank=True,null=True)
    added_by = models.ForeignKey("healthcare.UserMaster",related_name='symptoms_details_added_by',on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey("healthcare.UserMaster",related_name='symptoms_details_updated_by',on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "symptom_details"

class TransactionMaster(models.Model):
    appointment = models.ForeignKey("healthcare.AppointmentMaster",related_name='appointment_payment',on_delete=models.CASCADE,null=True)
    amount = models.CharField(max_length=25)
    razorpay_order_id = models.CharField(max_length=200,null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=200,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=500,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True, null=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "transaction_master"


