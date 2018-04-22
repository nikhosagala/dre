from django.urls import path

from employee import views, ajax

app_name = 'employee'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('home', views.home, name='home'),
    path('evaluation/<int:employee_id>', views.evaluation, name='employee-evaluation'),
    path('evaluation/result', views.evaluation_result, name='evaluation-result'),
    path('promotion/<int:employee_id>', views.promotion, name='employee-promotion')
]

urlpatterns += [
    path('ajax-employee-list', ajax.employee_list, name='ajax-employee-list'),
    path('ajax-evaluation-list/<int:employee_id>', ajax.employee_evaluation, name='ajax-evaluation-list'),
    path('ajax-promotion-list/<int:employee_id>', ajax.employee_promotion, name='ajax-promotion-list'),
    path('ajax-result-list', ajax.employee_evaluation_result, name='ajax-result-list')
]
