from django.urls import path

from employee import views, ajax

app_name = 'employee'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('evaluation/<int:employee_id>', views.evaluation, name='employee-evaluation'),
    path('evaluation/result', views.evaluation_result, name='evaluation-result')
]

urlpatterns += [
    path('ajax-employee-list', ajax.employee_list, name='ajax-employee-list'),
    path('ajax-question-list/<int:employee_id>', ajax.employee_evaluation, name='ajax-question-list'),
    path('ajax-result-list', ajax.employee_evaluation_result, name='ajax-result-list')
]
