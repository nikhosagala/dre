from django.urls import path

from employee import views, ajax

app_name = 'employee'

urlpatterns = [
    path('', views.dashboard, name='dashboard')
]

urlpatterns += [
    path('ajax', ajax.employee_list, name='ajax-employee-list')
]
