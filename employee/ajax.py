import http
import json

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from employee.helpers import assestment_productivity, get_result_by_supervisor, assestment_promotion, \
    get_result_by_employee
from employee.models import Employee, Parameter, Answer, Result
from employee.validators import ValidatorResultAdd, AnswerValidator


@csrf_exempt
def employee_list(request):
    user = request.user
    employees = Employee.objects.filter(supervisor=user).all()
    return JsonResponse([{
        'full_name': employee.first_name + ' ' + employee.last_name,
        'nik': employee.nik,
        'email': employee.email,
        'assestment': {
            'link': reverse('employee:assestment-detail', kwargs={'employee_id': employee.id})
        },
        'promotion': {
            'link': reverse('employee:promotion-detail', kwargs={'employee_id': employee.id})
        }
    } for employee in employees], safe=False, status=http.HTTPStatus.OK)


@csrf_exempt
def employee_assestment(request, employee_id):
    if request.method == 'GET':
        employee = Employee.objects.get(pk=employee_id)
        questions = Parameter.objects.filter(department=employee.department).all()
        return JsonResponse([{
            'id': question.id,
            'question': question.question,
            'weight': question.weight,
            'standard': question.standard
        } for question in questions], safe=False, status=http.HTTPStatus.OK)
    if request.method == 'POST':
        employee = Employee.objects.get(pk=employee_id)
        body = json.loads(request.body.decode('utf-8'))

        validate = ValidatorResultAdd(body)
        if validate.is_valid():
            try:
                with transaction.atomic():
                    answers = body.get('answers')
                    period = validate.cleaned_data['period']

                    result, created = Result.objects.get_or_create(employee=employee, period=period)

                    for answer in answers:
                        question = Parameter.objects.get(pk=answer.get('question').get('id'))
                        created_answer = Answer.objects.create(question=question, value=answer.get('value'))
                        result.answers.add(created_answer)

                    assestment_productivity(result)

                    return JsonResponse({
                        'message': 'Ok'
                    }, status=http.HTTPStatus.CREATED)
            except Exception as e:
                return JsonResponse({
                    'message': 'Internal server error',
                    'error': f'{e}'
                }, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

        return JsonResponse({
            'message': 'Your data is invalid.'
        }, status=http.HTTPStatus.BAD_REQUEST)


@csrf_exempt
def result(request):
    user = request.user
    results = []
    if user.is_superuser:
        results = get_result_by_supervisor(user)
    elif user.is_staff:
        results = get_result_by_employee(user)
    return JsonResponse([{
        'full_name': result.employee.first_name + ' ' + result.employee.last_name,
        'nik': result.employee.nik,
        'result': result.result,
        'period': result.period,
    } for result in results], safe=False, status=http.HTTPStatus.OK)


@csrf_exempt
def employee_promotion(request, employee_id):
    if request.method == 'GET':
        employee = Employee.objects.get(pk=employee_id)
        questions = Parameter.objects.filter(department=employee.department).all()
        return JsonResponse([{
            'id': question.id,
            'question': question.question,
            'weight': question.weight,
        } for question in questions], safe=False, status=http.HTTPStatus.OK)
    if request.method == 'POST':
        employee = Employee.objects.get(pk=employee_id)
        body = json.loads(request.body.decode('utf-8'))

        validate = ValidatorResultAdd(body)
        if validate.is_valid():
            try:
                with transaction.atomic():
                    answers = body.get('answers')
                    period = validate.cleaned_data['period']

                    result = Result.objects.create(employee=employee, period=period)

                    for answer in answers:
                        question = Parameter.objects.get(pk=answer.get('question').get('id'))
                        answer_val = AnswerValidator(answer)
                        if answer_val.is_valid():
                            created_answer = Answer.objects.create(question=question,
                                                                   value=answer_val.cleaned_data['value'])
                            result.answers.add(created_answer)

                    assestment_promotion(result)

                    return JsonResponse({
                        'message': 'Ok',
                        'standart': settings.STANDARD
                    }, status=http.HTTPStatus.CREATED)
            except Exception as e:
                return JsonResponse({
                    'message': 'Internal server error',
                    'error': f'{e}'
                }, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

        return JsonResponse({
            'message': 'Your data is invalid.'
        }, status=http.HTTPStatus.BAD_REQUEST)
