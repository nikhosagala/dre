from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy, reverse

from employee.models import Employee


@staff_member_required(login_url=reverse_lazy('admin:login'))
def homepage(request):
    return render(request, 'employee/homepage.html')


@staff_member_required(login_url=reverse_lazy('admin:login'))
def assestment(request):
    return render(request, 'employee/assestment.html')


@staff_member_required(login_url=reverse_lazy('admin:login'))
def promotion(request):
    return render(request, 'employee/promotion.html')


@staff_member_required(login_url=reverse_lazy('admin:login'))
def assestment_detail(request, employee_id):
    try:
        employee = Employee.objects.get(pk=employee_id)
        assestment_url = reverse('employee:ajax-assestment-detail', kwargs={'employee_id': employee.id})
    except Employee.DoesNotExist:
        raise Http404('Employee does not exist')
    return render(request, 'employee/assestment-detail.html',
                  {'employee': employee,
                   'assestment_url': assestment_url
                   })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def result(request):
    return render(request, 'employee/result.html')


@staff_member_required(login_url=reverse_lazy('admin:login'))
def promotion_detail(request, employee_id):
    try:
        employee = Employee.objects.get(pk=employee_id)
        promotion_url = reverse('employee:ajax-promotion-detail', kwargs={'employee_id': employee.id})
    except Employee.DoesNotExist:
        raise Http404('Employee does not exist')
    return render(request, 'employee/promotion-detail.html',
                  {'employee': employee,
                   'promotion_url': promotion_url
                   })
