from employee.models import Result, Employee, Answer, Department, Parameter


def assestment_productivity(result: Result):
    supervisor = result.employee.supervisor
    total_assestment = 0
    for question in get_all_available_question(supervisor.department):
        assestment_per_question = []
        for result_employee in get_result_by_supervisor(supervisor, result.period):
            for answer in result_employee.answers.filter(question=question):
                assestment_per_question.append(validation(answer.value, answer.question.standard))
        normalization = max(assestment_per_question)
        criteria = 0
        if normalization > 0:
            answer = result.answers.filter(question=question).first()
            criteria = float(validation(answer.value, answer.question.standard) / normalization)
        weight = float(answer.question.weight) / 100
        total_assestment += (criteria * weight)
    if total_assestment > 0.999:
        result.result = Result.PRODUCTIVE
    else:
        result.result = Result.NOT_PRODUCTIVE
    result.save()


def validation(value, weight):
    if value >= weight:
        return 1
    else:
        return 0


def get_result_by_supervisor(supevisor: Employee, period=None):
    if period:
        results = Result.objects.filter(employee__supervisor=supevisor, period__icontains=period)
    else:
        results = Result.objects.filter(employee__supervisor=supevisor)
    return results


def get_all_available_question(department: Department):
    results = Parameter.objects.filter(department=department)
    return results
