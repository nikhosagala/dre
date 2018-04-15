from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

from employee.models import Employee


@staff_member_required
def employee_list(request):
    user = request.user
    employees = Employee.objects.filter(supervisor=user).all()
    return JsonResponse([{
        'full_name': employee.first_name + ' ' + employee.last_name,
        'nik': employee.nik
    } for employee in employees], safe=False)
