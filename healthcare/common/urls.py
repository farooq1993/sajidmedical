from healthcare.common import views
from django.urls import re_path, path

urlpatterns = [
    re_path(r'^send_otp/$',views.SendOTP.as_view(),name='send_otp'),
    # re_path(r'^user_registration/$',views.UserRegistration.as_view(),name='send_otp'),
    path('user_registration/', views.UserRegistration.as_view(), name='send_otp'),
    re_path(r'^login_by_otp/$',views.LoginByOTP.as_view(),name='login_by_otp'),
    # re_path(r'^login_by_password/$',views.LoginByPassword.as_view(),name='login_by_password'),
    path('login_by_password/',views.LoginByPassword.as_view(),name='login_by_password'),
    re_path(r'^logout/$',views.Logout.as_view(),name='send_otp'),
    re_path(r'^get_freesearch_token/$',views.GetFreeseachToken.as_view(),name='get_freesearch_token'),
    re_path(r'^get_appointment/$',views.GetAppointment.as_view(),name='send_otp'),
    re_path(r'^set_password/$',views.SetPassword.as_view(),name='set_password'),
    re_path(r'^reset_password/$',views.ResetPassword.as_view(),name='reset_password'),
    re_path(r'^manage_appointment/$',views.ManageAppointment.as_view(),name='manage_appointment'),
    re_path(r'^refresh_token/$',views.RefreshToken.as_view(),name='refresh_token'),
    re_path(r'^update_personal_details/$',views.UpdatePersonalDetails.as_view(),name='update_personal_details'),
    re_path(r'^generate_prescription_pdf/$',views.GeneratePrescriptionPdf.as_view(),name='generate_prescription_pdf'),
    re_path(r'^get_patient_list/$',views.GetPatientList.as_view(),name='get_patient_list'),
    re_path(r'^get_doctor_list/$',views.GetDoctorList.as_view(),name='get_doctor_list'),
    re_path(r'^proceed_payment/$',views.ProceedPayment.as_view(),name='proceed_payment'),
    re_path(r'^payment_success/$',views.PaymentSuccess.as_view(),name='payment_success'),
    re_path(r'^get_symptoms/$',views.GetSymptoms.as_view(),name='get_symptoms'),
    re_path(r'^add_test/$',views.AddTest.as_view(),name='add_test'),
    re_path(r'^get_test/$',views.GetTest.as_view(),name='get_test'),
    re_path(r'^get_prescription/$',views.GetPrescription.as_view(),name='get_prescription'),


]
