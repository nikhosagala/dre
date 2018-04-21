from django.urls import path

from employee import views, ajax

app_name = 'employee'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('evaluation/<int:employee_id>', views.evaluation, name='employee-evaluation'),
]

urlpatterns += [
    path('ajax-employee-list', ajax.employee_list, name='ajax-employee-list'),
    path('ajax-question-list/<int:employee_id>', ajax.employee_evaluation, name='ajax-question-list')
]
