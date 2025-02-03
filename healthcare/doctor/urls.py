from healthcare.doctor import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^get_profile/$',views.GetProfile.as_view(),name='get_profile'),
    re_path(r'^create_appointment/$',views.CreateAppointment.as_view(),name='create_appointment'),
    re_path(r'^add_staff/$',views.AddStaff.as_view(),name='add_staff'),
    re_path(r'^get_staff/$',views.GetStaff.as_view(),name='get_staff'),
    re_path(r'^manage_staff/$',views.ManageStaff.as_view(),name='manage_staff'),
    re_path(r'^add_medicine/$',views.AddMedicine.as_view(),name='add_medicine'),
    re_path(r'^get_medicine/$',views.GetMedicine.as_view(),name='get_medicine'),
    re_path(r'^manage_medicine/$',views.ManageMedicine.as_view(),name='manage_medicine'),
    re_path(r'^create_prescription/$',views.CreatePrescription.as_view(),name='create_prescription'),
    re_path(r'^get_prescription/$',views.GetPrescription.as_view(),name='get_prescription'),
    re_path(r'^manage_prescription/$',views.ManagePrescription.as_view(),name='manage_prescription'),
    re_path(r'^manage_account/$',views.ManageAccount.as_view(),name='manage_account'),
    re_path(r'^get_staff_profile/$',views.GetStaffProfile.as_view(),name='get_staff_profile'),
]
