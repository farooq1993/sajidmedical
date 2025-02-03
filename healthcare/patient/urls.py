from healthcare.patient import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^get_profile/$',views.GetProfile.as_view(),name='get_profile'),
    re_path(r'^create_appointment/$',views.CreateAppointment.as_view(),name='create_appointment'),
    re_path(r'^add_family_member/$',views.AddFamilyMember.as_view(),name='add_family_member'),
    re_path(r'^get_family_member/$',views.GetFamilyDetails.as_view(),name='get_family_member'),
    re_path(r'^manage_family_member/$',views.ManageFamilyMember.as_view(),name='manage_family_member'),
    re_path(r'^manage_account/$',views.ManageAccount.as_view(),name='manage_account'),
]