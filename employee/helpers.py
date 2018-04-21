from employee.models import Result, Employee


def assestment(result: Result):
    supervisor = result.employee.supervisor
    employees = supervisor.employees.all()
    all_assignment = []
    total_assestment = 0
    for employee in employees:
        for result_employee in get_result_by_employee(employee, result.period):
            if result_employee.answers.all():
                for answer in result_employee.answers.all():
                    all_assignment.append(validation(answer.value, answer.question.standard))
    normalization = max(all_assignment)
    for result_update in result.answers.all():
        criteria = float(validation(result_update.value, result_update.question.standard) / normalization)
        weight = float(result_update.question.weight) / 100
        total_assestment += (criteria * weight)
    if total_assestment > 0.999:
        result.result = Result.PRODUCTIVE
    result.save()


def validation(value, weight):
    if value >= weight:
        return 1
    else:
        return 0


def get_result_by_employee(employee: Employee, period=None):
    if period:
        results = Result.objects.filter(employee=employee, period__icontains=period)
    else:
        results = Result.objects.filter(employee=employee)
    return results
