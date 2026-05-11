from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from .ai_services import (
    generate_workforce_insights
)

from .services import (
    get_dashboard_metrics
)

from .document_services import (
    extract_text_from_pdf
)

from .ai_services import (
    analyze_resume_text
)

from .models import Employee
from .forms import EmployeeForm
from django.contrib import messages


class EmployeeListView(LoginRequiredMixin,ListView):

    model = Employee

    template_name = (
        'employees/employee_list.html'
    )

    context_object_name = 'employees'

    paginate_by = 5

    def get_queryset(self):

        queryset = Employee.objects.filter(
            created_by=self.request.user
        )

        search = self.request.GET.get(
            'search'
        )

        department = self.request.GET.get(
            'department'
        )

        if search:
            queryset = queryset.filter(
                first_name__icontains=search
            )

        if department:
            queryset = queryset.filter(
                department__icontains=department
            )

        return queryset


@login_required
def employee_list(request):

    employees = Employee.objects.filter(created_by=request.user)

    return render(
        request,
        'employees/employee_list.html',
        {
            'employees': employees
        }
    )
@login_required
def create_employee(request):

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            employee = form.save(commit=False)

            employee.created_by = request.user

            employee.save()

            messages.success(
                request,
                'Employee created successfully.'
            )

            return redirect('employee_list')

    else:

        form = EmployeeForm()

    return render(
        request,
        'employees/create_employee.html',
        {
            'form': form
        }
    )

@login_required
def employee_detail(
    request,
    employee_id
):

    employee = get_object_or_404(
        Employee,
        id=employee_id
    )
    resume_analysis = None

    if employee.resume:

        file_path = employee.resume.path

        if file_path.endswith('.pdf'):
            resume_text = (
                extract_text_from_pdf(
                    file_path
                )
            )

            resume_analysis = (
                analyze_resume_text(
                    resume_text
                )
            )

    return render(
        request,
        'employees/employee_detail.html',
        {
            'employee': employee,
            'resume_analysis': resume_analysis
        }
    )

@login_required
def edit_employee(
    request,
    employee_id
):

    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            instance=employee
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Employee updated successfully.'
            )

            return redirect(
                'employee_detail',
                employee_id=employee.id
            )

    else:

        form = EmployeeForm(
            instance=employee
        )

    return render(
        request,
        'employees/edit_employee.html',
        {
            'form': form,
            'employee': employee
        }
    )

@login_required
def delete_employee(
    request,
    employee_id
):

    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    if request.method == 'POST':

        employee.delete()

        messages.success(
            request,
            'Employee deleted successfully.'
        )

        return redirect(
            'employee_list'
        )

    return render(
        request,
        'employees/delete_employee.html',
        {
            'employee': employee
        }
    )

@login_required
def dashboard(request):

    employees = Employee.objects.filter(
        created_by=request.user
    )

    metrics = get_dashboard_metrics(
        employees
    )

    ai_insights = (
        generate_workforce_insights(
            employees
        )
    )

    return render(
        request,
        'employees/dashboard.html',
        {
            **metrics,
            'ai_insights': ai_insights
        }
    )