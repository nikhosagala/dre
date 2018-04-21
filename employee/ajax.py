from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.urls import reverse

from employee.models import Employee, Parameter


@staff_member_required
def employee_list(request):
    user = request.user
    employees = Employee.objects.filter(supervisor=user).all()
    return JsonResponse([{
        'full_name': employee.first_name + ' ' + employee.last_name,
        'nik': employee.nik,
        'email': employee.email,
        'evaluation': {
            'link': reverse('employee:employee-evaluation', kwargs={'employee_id': employee.id})
        }
    } for employee in employees], safe=False)


@staff_member_required()
def employee_evaluation(request, employee_id):
    if request.method == 'GET':
        employee = Employee.objects.get(pk=employee_id)
        questions = Parameter.objects.filter(department=employee.department).all()
        return JsonResponse([{
            'question': question.question,
            'weight': question.weight
        } for question in questions], safe=False)
