from django.urls import path

from employee import views, ajax

app_name = 'employee'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('assestment', views.assestment, name='assestment'),
    path('assestment/<int:employee_id>', views.assestment_detail, name='assestment-detail'),
    path('promotion', views.promotion, name='promotion'),
    path('promotion/<int:employee_id>', views.promotion_detail, name='promotion-detail'),
    path('result', views.result, name='result'),
]

urlpatterns += [
    path('ajax-employee-list', ajax.employee_list, name='ajax-employee-list'),
    path('ajax-assestment-detail/<int:employee_id>', ajax.employee_assestment, name='ajax-assestment-detail'),
    path('ajax-promotion-detail/<int:employee_id>', ajax.employee_promotion, name='ajax-promotion-detail'),
    path('ajax-result-list', ajax.result, name='ajax-result-list')
]
