from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy, reverse

from employee.models import Employee


@staff_member_required(login_url=reverse_lazy('admin:login'))
def dashboard(request):
    return render(request, 'employee/dashboard.html')


@staff_member_required(login_url=reverse_lazy('admin:login'))
def evaluation(request, employee_id):
    try:
        employee = Employee.objects.get(pk=employee_id)
        evaluation_url = reverse('employee:ajax-question-list', kwargs={'employee_id': employee.id})
    except Employee.DoesNotExist:
        raise Http404('Employee does not exist')
    return render(request, 'employee/evaluation.html',
                  {'employee': employee,
                   'evaluation_url': evaluation_url
                   })


def evaluation_result(request):
    return render(request, 'employee/evaluation_result.html')
