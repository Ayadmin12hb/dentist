from django.urls import path
from . import views
from django.urls import include

app_name = 'dentist'

urlpatterns = [
    path('', views.home, name='home'),
    path('branch_offices/', views.branch_offices_list, name='branch_offices_list'),
    path('branch_offices/detail/<int:pk>', views.BranchOfficeDetail.as_view(), name='branch_offices_detail'),
    path('branch_offices/update/<int:pk>', views.BranchOfficeUpdate.as_view(), name='branch_offices_update'),
    path('branch_offices/delete/<int:pk>', views.BranchOfficeDelete.as_view(), name='branch_offices_delete'),
    path('branch_offices/add/', views.branch_offices_add, name='branch_offices_add'),

    path('<int:pk>/delete/', views.delete_branch_office, name='delete_branch_office'),
    path('patients/', views.patients_list, name='patients_list'),
    path('patients/add/', views.patients_add, name='patients_add'),

    path('users/', views.user_list, name='user_list'),
    path('personel/', views.personel_list, name='personel_list'),
    path('personel/add/', views.PersonelAdd.as_view(), name='personel_add'),
    path('personel/add/<int:pk>', views.PersonelAddContinue.as_view(), name='personel_add_continue'),
    path('personel/update/<int:pk>', views.PersonelUpdate.as_view(), name='personel_update'),
    path('personel/delete/<int:pk>', views.PersonelDelete.as_view(), name='personel_delete'),

    path('visits/', views.visits_list, name='visits_list'),
    path('visits/add/', views.visits_add, name='visits_add'),
    path('visits/update/<int:pk>', views.VisitUpdate.as_view(), name='visit_update'),
    path('visits/delete/<int:pk>', views.VisitDelete.as_view(), name='visit_delete'),
    path('visits/detail/<int:pk>', views.VisitDetail.as_view(), name='visit_detail'),

    path('EngagementsCalendar/', views.EngagementsCal, name='EngagementsCal'),

    path('password/', views.ChangePasswordView.as_view(), name='new_password'),
    # path('password_changes', views.password_changes, name='password_changes'),
    ]
