from django.db.models import Avg, Max


def get_dashboard_metrics(
    employees
):

    return {

        'total_employees':
            employees.count(),

        'departments':
            employees.values(
                'department'
            ).distinct().count(),

        'average_salary':
            employees.aggregate(
                Avg('salary')
            )['salary__avg'],

        'highest_salary':
            employees.aggregate(
                Max('salary')
            )['salary__max']
    }