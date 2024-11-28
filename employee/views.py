from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from admin_panel.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse



def employee_dashboard(request):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        # Redirect to login if session is not set
        return redirect('employee:login')

    try:
        employee = Employee.objects.get(id=employee_id)
        tasks = WorksiteAssignment.objects.filter(employee=employee).select_related('worksite')
        context = {'tasks': tasks}
        return render(request, 'employee/dashboard.html', context)
    except Employee.DoesNotExist:
        return redirect('employee:login')


def login(request):
    next_url = request.GET.get('next')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            # Check if an employee with the given username and password exists
            employee = Employee.objects.get(username=username, password=password)
            # Log in the employee manually by creating a session
            request.session['employee_id'] = employee.id  # Store the employee ID in the session
            return redirect(next_url if next_url else 'employee:employee_dashboard')
        except Employee.DoesNotExist:
            messages.error(request, "Invalid login credentials.")

    return render(request, 'employee/login.html')

def view_worksite(request, work_id):
    
        worksite = Work.objects.get(id=work_id)

        # Serialize the worksite data
        worksite_data = {
            'title': worksite.title,
            'description': worksite.description,
            'customer': worksite.customer.name,  # Assuming Customer has a 'name' field
            'type_of_work': worksite.type_of_work,
            'start_date': worksite.start_date,
            'end_date': worksite.end_date,
            'status': worksite.status,
            'priority': worksite.priority,
            
            
        }

        return JsonResponse(worksite_data)

def update_work(request, work_id):
    if request.method == 'POST':
        update_text = request.POST.get('update_text')
        work_image = request.FILES.get('work_image')
        employee_id = request.session.get('employee_id')
        employee = Employee.objects.get(id=employee_id)
        
        DailyUpdate.objects.create(
            work_id=work_id,
            employee=employee,
            update_text=update_text,
            work_image=work_image
        )
        return redirect('employee:employee_dashboard')

    return render(request, 'employee/update_work.html', {'work_id': work_id})

def talk_to_admin(request, work_id):
    if request.method == 'POST':
        message = request.POST.get('message')
        employee_id = request.session.get('employee_id')
        employee = Employee.objects.get(id=employee_id)
        AdminMessage.objects.create(
            work_id=work_id,
            employee=employee,
            message=message
        )
        return redirect('employee:employee_dashboard')

    return render(request, 'employee/talk_to_admin.html', {'work_id': work_id})

def logout_view(request):
    logout(request)
    request.session.flush() 
    return redirect('employee:login')