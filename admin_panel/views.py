from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from decimal import Decimal
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime, timedelta
from django.db.models import Sum
from django.core.files.storage import FileSystemStorage


# Registration/Login View
def register_or_login(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if action == 'register':
            email = request.POST.get('email')
            name = request.POST.get('name')
            age = request.POST.get('age')

            if AdminCredentials.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            else:
                # Hash the password before saving
                hashed_password = make_password(password)
                AdminCredentials.objects.create(
                    username=username,
                    password=hashed_password,
                    email=email,
                    name=name,
                    age=age
                )
                messages.success(request, "Registration successful!")
                return redirect('register_or_login')  # Redirect to the same page for login

        elif action == 'login':
            try:
                admin = AdminCredentials.objects.get(username=username)
                if check_password(password, admin.password):
                    # Set session data
                    request.session['user_id'] = admin.id
                    request.session['user_role'] = 'admin'  # Assign a role for admin
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid credentials.")
            except AdminCredentials.DoesNotExist:
                messages.error(request, "Invalid credentials.")
    
    return render(request, 'register_login.html')



def dashboard(request):
    works = Work.objects.all().select_related('customer')  # Use select_related to optimize queries

    # Filters
    search_query = request.GET.get('search', '')
    if search_query:
        works = works.filter(customer__name__icontains=search_query)  # Updated to filter by customer name

    # Filtering and sorting options
    filter_status = request.GET.get('filter_status')
    if filter_status:
        works = works.filter(status=filter_status)
    
    filter_priority = request.GET.get('filter_priority')
    if filter_priority:
        works = works.filter(priority=filter_priority)  # Add filtering for priority
    
    sort_by = request.GET.get('sort_by', 'created_at')
    if sort_by == 'start_date':
        works = works.order_by('start_date')
    elif sort_by == '-start_date':
        works = works.order_by('-start_date')
    else:
        works = works.order_by(sort_by)

    print(works)
    context = {
        'works': works,
        'search_query': search_query,
        'filter_priority': filter_priority,
        'filter_status': filter_status,
        'sort_by': sort_by,
    }
    return render(request, 'dashboard.html', context)



def get_upcoming_deadlines(request):
    # Calculate the date range for the next week
    today = datetime.today()
    next_week = today + timedelta(days=7)

    # Fetch worksites with end dates within the next week
    worksites_with_deadlines = Work.objects.filter(end_date__range=(today, next_week))

    # Prepare the data to return
    worksites_data = []
    for worksite in worksites_with_deadlines:
        worksites_data.append({
            'title': worksite.title,
            'customer_name': worksite.customer.name,  # Adjust based on your model relationship
            'start_date': worksite.start_date.strftime('%Y-%m-%d'),
            'end_date': worksite.end_date.strftime('%Y-%m-%d'),
            'status': worksite.status,
        })

    return JsonResponse({'reminder': worksites_data})


@login_required
def profile_view(request):
    user = request.user  # Get the logged-in user
    
    print(f"Authenticated user: {user}")  # Check if user is authenticated

    if request.method == "POST":
        print("POST request received.")
        
        # Retrieve and validate updated data
        username = request.POST.get("username", user.username)
        email = request.POST.get("email", user.email)
        contact_number = request.POST.get("contact_number", user.contact_number)
        
        # Basic validation
        if not username:
            messages.error(request, "Username cannot be empty.")
            return render(request, "profile.html", {"user": user})
        
        if not email:
            messages.error(request, "Email cannot be empty.")
            return render(request, "profile.html", {"user": user})

        # Save updated data
        user.username = username
        user.email = email
        user.contact_number = contact_number  # Custom field
        user.save()
        
        messages.success(request, "Profile updated successfully.")
        print(f"Updated user details: {user.username}, {user.email}, {user.contact_number}")
        return redirect("profile")

    return render(request, "profile.html", {"user": user})

def add_work(request):
    if request.method == "POST":
        # Customer fields
        name = request.POST.get("name")
        address = request.POST.get("address")
        location = request.POST.get("location")
        contact_number = request.POST.get("contact_number")
        email = request.POST.get("email")

        # Work fields
        title = request.POST.get("title")
        description = request.POST.get("description")
        type_of_work = ', '.join([value for key, value in request.POST.items() if key == "work_type"])
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        if(request.POST.get("actual_end_date")):
            actual_end_date = request.POST.get("actual_end_date")
        status = request.POST.get("status")
        priority = request.POST.get("priority")
        action = request.POST.get("action")
        commitment = request.POST.get("commitment")
        remark = request.POST.get("remark")
        total_amount = request.POST.get("total_amount")
        floor_plans = request.FILES.getlist("floor_plans")  # Get list of uploaded floor plans
        other_documents = request.FILES.getlist("other_documents")  # Get list of uploaded other documents

        # Create Customer object
        customer = Customer.objects.create(
            name=name,
            address=address,
            location=location,
            contact_number=contact_number,
            email=email,
            created_at=timezone.now()
        )
        if(request.POST.get("actual_end_date")):
            # Create Work object
            work = Work.objects.create(
                customer=customer,
                title=title,
                description=description,
                type_of_work=type_of_work,
                start_date=start_date,
                end_date=end_date,
                actual_end_date=actual_end_date,
                status=status,
                priority=priority,
                action=action,
                commitment=commitment,
                remark=remark,
                total_amount=total_amount,
                created_at=timezone.now()
            )
        else:
            # Create Work object
            work = Work.objects.create(
                customer=customer,
                title=title,
                description=description,
                type_of_work=type_of_work,
                start_date=start_date,
                end_date=end_date,
                status=status,
                priority=priority,
                action=action,
                commitment=commitment,
                remark=remark,
                total_amount=total_amount,
                created_at=timezone.now()
            )
        # Handle floor plan uploads
        for file in floor_plans:
            FloorPlan.objects.create(work=work, file=file)

        # Save multiple other documents
        for doc in other_documents:
            OtherDocument.objects.create(work=work, file=doc)

        return redirect('dashboard') # Adjust redirection as needed

    return render(request, 'add_worksite.html')



def edit_work(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    customer = get_object_or_404(Customer, id=work.customer.id)  # Fetch customer details

    if request.method == 'POST':
        # Fetching and updating the worksite fields
        work.customer.name = request.POST.get('name')  
        work.customer.location = request.POST.get('location')  
        work.customer.contact_number = request.POST.get('contact_number')  
        work.customer.email = request.POST.get('email')  

        work.start_date = request.POST.get('start_date')
        work.end_date = request.POST.get('end_date')
        work.actual_end_date = request.POST.get('actual_end_date')
        work.title = request.POST.get("title")

        # Handling the work types (checkbox values)
        work_types = request.POST.getlist('work_type')  
        work.type_of_work = ', '.join(work_types)  

        work.priority = request.POST.get('priority')
        work.status = request.POST.get('status')  

        # Updating commitment and remark fields
        work.commitment = request.POST.get('commitment')
        work.remark = request.POST.get('remark')
        
        work.total_amount = request.POST.get("total_amount")

        # Handle floor plan uploads
        if request.FILES.getlist('floor_plans'):
            floor_plans = request.FILES.getlist("floor_plans")
            for file in floor_plans:
                FloorPlan.objects.create(work=work, file=file)

        # Handle other document uploads
        if request.FILES.getlist('other_documents'):
            other_documents = request.FILES.getlist("other_documents")
            for doc in other_documents:
                OtherDocument.objects.create(work=work, file=doc)

        # Handle deletion of floor plans
        for floor_plan in work.floor_plans.all():
            if f'delete_floor_plan_{floor_plan.id}' in request.POST:
                floor_plan.file.delete()  # Delete the file from storage
                floor_plan.delete()  # Delete the record

        # Handle deletion of other documents
        for doc in work.other_documents.all():
            if f'delete_document_{doc.id}' in request.POST:
                doc.file.delete()  # Delete the file from storage
                doc.delete()  # Delete the record

        # Save the updated work object
        work.save()

        # Redirect to the dashboard after saving
        return redirect('dashboard')

    # Fetch floor plans and other documents for the template
    floor_plans = work.floor_plans.all()
    other_documents = work.other_documents.all()

    # Render the template with the current worksite data, including customer details
    return render(request, 'edit_worksite.html', {
        'work': work,
        'customer': customer,
        'floor_plans': floor_plans,
        'other_documents': other_documents
    })



def delete_work(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    work.delete()
    return redirect('dashboard')

def view_payments(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    payments = Payment.objects.filter(work=work)

    # Calculate the total received payments
    total_received = sum(payment.amount for payment in payments)

    # Calculate the remaining amount
    remaining_amount = work.total_amount - total_received

    # Pass these values to the template
    context = {
        'work': work,
        'payments': payments,
        'total_amount': work.total_amount,
        'total_received': total_received,
        'remaining_amount': remaining_amount
    }
    return render(request, 'view_payments.html', context)

def add_payment(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        payment_method = request.POST.get('payment_method')
        reference_number = request.POST.get('reference_number')
        
        Payment.objects.create(
            work=work,
            amount=Decimal(amount),
            payment_date=payment_date,
            payment_method=payment_method,
            reference_number=reference_number
        )
        return redirect('view_payments', work_id=work.id)
    return render(request, 'add_payment.html', {'work': work})



def work_details(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    # Get assigned employees
    assignments = work.assignments.all()  # Using the related_name 'assignments'
    assigned_employees = [assignment.employee.name for assignment in assignments]

    data = {
        'id': work.id,
        'customer_name': work.customer.name,
        'description': work.description,
        'type_of_work': work.type_of_work,
        'start_date': work.start_date.strftime('%Y-%m-%d'),
        'end_date': work.end_date.strftime('%Y-%m-%d') if work.end_date else 'N/A',
        'priority': work.priority,
        'status': work.status,
        'contact_number': work.customer.contact_number,  # Make sure this field exists in your Customer model
        'location': work.customer.location,  # Ensure this field exists in your Customer model
        'work_type': work.type_of_work,
        'assigned_employees': assigned_employees,
        'total_amount': work.total_amount
    }
    return JsonResponse(data)



def add_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        location = request.POST.get('location')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        
        Customer.objects.create(
            name=name,
            address=address,
            location=location,
            contact_number=contact_number,
            email=email
        )
        return redirect('dashboard')
    return render(request, 'add_customer.html')

def add_supplier(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        category = request.POST.get('category')
        
        Supplier.objects.create(
            name=name,
            location=location,
            category=category
        )
        return redirect('dashboard')
    return render(request, 'add_supplier.html')



# Employee Registration and Management
def manage_employees(request):
    if request.method == 'POST':
        employee_code = request.POST['employee_code']
        name = request.POST['name']
        age = request.POST['age']
        address = request.POST['address']
        department = request.POST['department']
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = make_password(password)
        # Create new employee
        Employee.objects.create(employee_code=employee_code, name=name, age=age, address=address, department=department,username=username,
        password=hashed_password)
        messages.success(request, "Employee registered successfully!")
        return redirect('manage_employees')

    employees = Employee.objects.all()
    return render(request, 'manage_employees.html', {'employees': employees})
    
    
def logout_view(request):
    logout(request)
    return redirect("register_or_login")



# List Employees
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

# Add Employee
def add_employee(request):
    if request.method == 'POST':
        employee_code = request.POST['employee_code']
        name = request.POST['name']
        age = request.POST['age']
        address = request.POST['address']
        department = request.POST['department']
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = make_password(password)
        aadhar_number = request.POST.get('aadhar_number')
        pan_card_number = request.POST.get('pan_card_number')
        photo = request.FILES.get('photo')
        id_document = request.FILES.get('id_document')

        # Create Employee entry
        Employee.objects.create(
            employee_code=employee_code,
            name=name,
            age=age,
            address=address,
            department=department,
            username=username,
            password=hashed_password,
            aadhar_number=aadhar_number,
            pan_card_number=pan_card_number,
            photo=photo,
            id_document=id_document,
        )
        messages.success(request, "Employee added successfully!")
        return redirect('employee_list')

    return render(request, 'add_employee.html')

# Edit Employee
def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        employee.employee_code = request.POST['employee_code']
        employee.name = request.POST['name']
        employee.age = request.POST['age']
        employee.address = request.POST['address']
        employee.department = request.POST['department']
        employee.aadhar_number = request.POST.get('aadhar_number')
        employee.pan_card_number = request.POST.get('pan_card_number')

        if 'photo' in request.FILES:
            employee.photo = request.FILES['photo']

        if 'id_document' in request.FILES:
            employee.id_document = request.FILES['id_document']

        employee.save()
        messages.success(request, "Employee details updated successfully!")
        return redirect('employee_list')

    return render(request, 'edit_employee.html', {'employee': employee})
# Get Employee Details for Modal
def get_employee_details(request, id):
    
    employee = get_object_or_404(Employee, id=id)
    data = {
        'id': employee.id,
        'name': employee.name,
        'age': employee.age,
        'address': employee.address,
        'department': employee.department,
    }
    print(data)
    return JsonResponse(data)


def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('employee_list')  # Redirect to the employee list page after deletion


def assign_employee_to_worksite(request, worksite_id):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        worksite = get_object_or_404(Work, id=worksite_id)
        employee = get_object_or_404(Employee, id=employee_id)

        WorksiteAssignment.objects.create(worksite=worksite, employee=employee)
        return redirect('worksite_detail', worksite_id=worksite.id)  # Redirect to the worksite detail page
    
    
    
    
    
# def manage_assignments(request):
#     employees = Employee.objects.all()
#     worksites = Work.objects.all()

#     if request.method == "POST":
#         selected_worksite_id = request.POST.get('worksite_id')
#         selected_employee_id = request.POST.get('employee_id')

#         # Handle assignment from worksite selection
#         if selected_worksite_id:
#             worksite = get_object_or_404(Work, id=selected_worksite_id)
#             selected_employee_ids = request.POST.getlist('employee_ids')

#             # Assign selected employees to the worksite
#             if selected_employee_ids:
#                 for employee_id in selected_employee_ids:
#                     employee = get_object_or_404(Employee, id=employee_id)
#                     WorksiteAssignment.objects.get_or_create(worksite=worksite, employee=employee)

#             # Filter out assigned employees
#             assigned_employees = worksite.assignments.values_list('employee_id', flat=True)
#             available_employees = employees.exclude(id__in=assigned_employees)

#             return render(request, 'manage_assignments.html', {
#                 'employees': employees,
#                 'worksites': worksites,
#                 'selected_worksite': worksite,
#                 'available_employees': available_employees,
#             })

#         # Handle assignment from employee selection
#         if selected_employee_id:
#             employee = get_object_or_404(Employee, id=selected_employee_id)
#             selected_worksite_ids = request.POST.getlist('assign_worksite_ids')

#             # Assign selected worksites to the employee
#             if selected_worksite_ids:
#                 for worksite_id in selected_worksite_ids:
#                     worksite = get_object_or_404(Work, id=worksite_id)
#                     WorksiteAssignment.objects.get_or_create(worksite=worksite, employee=employee)

#             # Filter out assigned worksites
#             assigned_worksites = employee.assignments.values_list('worksite_id', flat=True)
#             available_worksites = worksites.exclude(id__in=assigned_worksites)

#             return render(request, 'manage_assignments.html', {
#                 'employees': employees,
#                 'worksites': worksites,
#                 'selected_employee': employee,
#                 'available_worksites': available_worksites,
#             })

#     context = {
#         'employees': employees,
#         'worksites': worksites,
#     }
#     return render(request, 'manage_assignments.html', context)





def manage_assignments(request):
    print("Received request to manage assignments")  # Log request receipt
    employees = Employee.objects.all()
    worksites = Work.objects.all()

    selected_worksite = None
    selected_employee = None
    available_employees = employees
    available_worksites = worksites

    if request.method == "POST":
        print("Received POST request")  # Log POST method
        selected_worksite_id = request.POST.get('worksite_id')
        selected_employee_id = request.POST.get('employee_id')

        print("Selected Worksite ID:", selected_worksite_id)  # Log selected worksite ID
        print("Selected Employee ID:", selected_employee_id)  # Log selected employee ID

        if selected_worksite_id:
            selected_worksite = get_object_or_404(Work, id=selected_worksite_id)
            selected_employee_ids = request.POST.getlist('employee_ids')
            if selected_employee_ids:
                for employee_id in selected_employee_ids:
                    employee = get_object_or_404(Employee, id=employee_id)
                    WorksiteAssignment.objects.get_or_create(worksite=selected_worksite, employee=employee)

            assigned_employees = selected_worksite.assignments.values_list('employee_id', flat=True)
            available_employees = employees.exclude(id__in=assigned_employees)
            selected_employee = None

        elif selected_employee_id:
            selected_employee = get_object_or_404(Employee, id=selected_employee_id)
            selected_worksite_ids = request.POST.getlist('assign_worksite_ids')
            if selected_worksite_ids:
                for worksite_id in selected_worksite_ids:
                    worksite = get_object_or_404(Work, id=worksite_id)
                    WorksiteAssignment.objects.get_or_create(worksite=worksite, employee=selected_employee)

            assigned_worksites = selected_employee.assignments.values_list('worksite_id', flat=True)
            available_worksites = worksites.exclude(id__in=assigned_worksites)
            selected_worksite = None

    context = {
        'employees': employees,
        'worksites': worksites,
        'selected_worksite': selected_worksite,
        'available_employees': available_employees,
        'selected_employee': selected_employee,
        'available_worksites': available_worksites,
    }
    return render(request, 'manage_assignments.html', context)
def get_worksite_assignments(request, worksite_id):
    # Fetch assignments for the specific worksite
    assignments = WorksiteAssignment.objects.filter(worksite_id=worksite_id).select_related('employee')
    assignment_list = [{
        'employee_name': assignment.employee.name,
        'date_assigned': assignment.date_assigned,
        'employee_id': assignment.employee.id
    } for assignment in assignments]

    # Get available employees (optional)
    available_employees = Employee.objects.exclude(id__in=assignments.values_list('employee_id', flat=True))

    return JsonResponse({
        'assignments': assignment_list,
        'available_employees': [{'id': emp.id, 'name': emp.name} for emp in available_employees]
    })

def get_employee_assignments(request, employee_id):
    # Fetch assignments for the specific employee
    assignments = WorksiteAssignment.objects.filter(employee_id=employee_id).select_related('worksite')
    assignment_list = [{
        'worksite_title': assignment.worksite.title,
        'date_assigned': assignment.date_assigned,
        'worksite_id': assignment.worksite.id
    } for assignment in assignments]

    # Get available worksites (optional)
    available_worksites = Work.objects.exclude(id__in=assignments.values_list('worksite_id', flat=True))

    return JsonResponse({
        'assignments': assignment_list,
        'available_worksites': [{'id': site.id, 'title': site.title} for site in available_worksites]
    })
    
    
    
    
def add_supplier(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        category = request.POST.get("category")

        Supplier.objects.create(name=name, location=location, category=category)
        return redirect("view_suppliers")

    return render(request, "add_supplier.html")


def view_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, "view_suppliers.html", {"suppliers": suppliers})


def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == "POST":
        supplier.name = request.POST.get("name")
        supplier.location = request.POST.get("location")
        supplier.category = request.POST.get("category")
        supplier.save()
        return redirect("view_suppliers")

    return render(request, "edit_supplier.html", {"supplier": supplier})


def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.delete()
    return redirect("view_suppliers")


def view_supplier_details(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    data = {
        "name": supplier.name,
        "location": supplier.location,
        "category": supplier.category,
        "created_at": supplier.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return JsonResponse(data)

def add_item(request):
    # Fetch unique categories from the Supplier table
    categories = Supplier.objects.values_list("category", flat=True).distinct()

    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        new_category = request.POST.get("new_category")
        supplier_id = request.POST.get("supplier")
        new_supplier = request.POST.get("new_supplier")
        price = request.POST.get("price")
        stock_quantity = request.POST.get("stock_quantity")

        # Add new category if provided
        if new_category:
            category = new_category

        # Create the item object with stock quantity
        item = Item.objects.create(name=name, category=category, price=price, stock_quantity=stock_quantity)

        # Add new supplier if provided
        if new_supplier:
            supplier = Supplier.objects.create(name=new_supplier, category=category)
            SupplierItem.objects.create(supplier=supplier, item=item)
        elif supplier_id:
            supplier = Supplier.objects.get(id=supplier_id)
            SupplierItem.objects.create(supplier=supplier, item=item)

        return redirect("view_items")

    return render(request, "add_item.html", {"categories": categories})



def get_suppliers(request):
    
    category = request.GET.get("category")
    suppliers = Supplier.objects.filter(category=category)
    suppliers_list = [{"id": supplier.id, "name": supplier.name} for supplier in suppliers]
    return JsonResponse({"suppliers": suppliers_list})



def view_items(request):
    items = Item.objects.all()
    
    # Prepare a list to hold items with their suppliers
    item_supplier_data = []
    
    for item in items:
        # Fetch suppliers for the current item
        suppliers = Supplier.objects.filter(supplieritem__item=item)
        supplier_names = ", ".join([supplier.name for supplier in suppliers])  # Concatenate supplier names
        item_supplier_data.append({
            "item": item,
            "suppliers": supplier_names
        })
    
    return render(request, "view_items.html", {"item_supplier_data": item_supplier_data})


def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    current_supplier = item.supplieritem_set.first().supplier if item.supplieritem_set.exists() else None
    categories = Supplier.objects.values_list("category", flat=True).distinct()

    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        new_category = request.POST.get("new_category")
        price = request.POST.get("price")
        stock_quantity = request.POST.get("stock_quantity")
        supplier_id = request.POST.get("supplier")
        new_supplier = request.POST.get("new_supplier")

        # Add new category if provided
        if new_category:
            category = new_category

        # Update item fields
        item.name = name
        item.category = category
        item.price = price
        item.stock_quantity = stock_quantity
        item.save()

        # Update or add a new supplier if provided
        if new_supplier:
            supplier = Supplier.objects.create(name=new_supplier, category=category)
            SupplierItem.objects.update_or_create(item=item, defaults={"supplier": supplier})
        elif supplier_id:
            supplier = Supplier.objects.get(id=supplier_id)
            SupplierItem.objects.update_or_create(item=item, defaults={"supplier": supplier})

        return redirect("view_items")

    return render(request, "edit_item.html", {
        "item": item,
        "categories": categories,
        "current_supplier": current_supplier
    })


def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect("view_items")

def view_item_details(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Fetch suppliers for the current item
    suppliers = Supplier.objects.filter(supplieritem__item=item)
    supplier_names = ", ".join([supplier.name for supplier in suppliers])  # Concatenate supplier names
    
    data = {
        "name": item.name,
        "category": item.category,
        "price": str(item.price),
        "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "suppliers": supplier_names  # Add suppliers to the response
    }
    
    return JsonResponse(data)








def generate_bill(request, worksite_id):
    worksite = get_object_or_404(Work, id=worksite_id)
    items = Item.objects.all()  # Fetch all items
    return render(request, 'generate_bill.html', {'worksite': worksite, 'items': items})

# def submit_bill(request):
#     if request.method == 'POST':
#         worksite_id = request.POST['worksite_id']
#         worksite = get_object_or_404(Work, id=worksite_id)
#         customer = worksite.customer

#         # Collect items and quantities
#         total_amount = Decimal('0.00')  # Initialize total_amount as Decimal
#         items_details = []
#         for item in Item.objects.all():
#             quantity = request.POST.get(f'item_quantity_{item.id}')
#             if quantity and int(quantity) > 0:
#                 quantity = Decimal(quantity)  # Convert quantity to Decimal
#                 amount = item.price * quantity  # Multiply Decimal by Decimal
#                 total_amount += amount
#                 items_details.append((item.name, quantity, item.price, amount))

#         # Handle discounts
#         discount_type = request.POST['discount_type']
#         discount_value = Decimal(request.POST['discount_value']) if request.POST['discount_value'] else Decimal('0.00')
#         if discount_type == 'percentage':
#             discount_amount = (discount_value / Decimal('100')) * total_amount
#         else:  # amount
#             discount_amount = discount_value
#         total_amount -= discount_amount

#         # Generate PDF
#         pdf_file = create_pdf(worksite, customer, items_details, discount_amount, total_amount)
#         # send_email_with_pdf(customer.email, pdf_file)

#         return redirect('dashboard')  # Redirect after processing
    


def submit_bill(request):
    if request.method == 'POST':
        worksite_id = request.POST['worksite_id']
        worksite = get_object_or_404(Work, id=worksite_id)
        customer = worksite.customer

        # Collect items and quantities
        total_amount = Decimal('0.00')  # Initialize total_amount as Decimal
        items_details = []
        for item in Item.objects.all():
            quantity = request.POST.get(f'item_quantity_{item.id}')
            if quantity and int(quantity) > 0:
                quantity = Decimal(quantity)  # Convert quantity to Decimal
                amount = item.price * quantity  # Multiply Decimal by Decimal
                total_amount += amount
                items_details.append((item.name, quantity, item.price, amount))
                
                item.stock_quantity -= quantity  # Decrease stock by the quantity in the bill
                item.save()

        # Handle discounts
        discount_type = request.POST['discount_type']
        discount_value = Decimal(request.POST['discount_value']) if request.POST['discount_value'] else Decimal('0.00')
        if discount_type == 'percentage':
            discount_amount = (discount_value / Decimal('100')) * total_amount
        else:  # amount
            discount_amount = discount_value
        total_amount -= discount_amount

        # Generate PDF
        pdf_file = create_pdf(worksite, customer, items_details, discount_amount, total_amount)

        # Serve the PDF
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bill.pdf"'  # For download
        return response  # Return the response to prompt download

        # Optional: You can redirect to the dashboard after downloading if needed
        # return redirect('dashboard')  
        
        
    
# def create_pdf(worksite, customer, items_details, discount_amount, total_amount):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="bill_{worksite.id}.pdf"'
    
#     p = canvas.Canvas(response, pagesize=letter)
#     width, height = letter
    
#     # Bill Header
#     p.drawString(100, height - 50, "Bill")
#     p.drawString(100, height - 70, f"Date: {timezone.now().strftime('%Y-%m-%d')}")
#     p.drawString(100, height - 90, f"Client Name: {customer.name}")
#     p.drawString(100, height - 110, f"Location: {customer.location}")
#     p.drawString(100, height - 130, f"Contact: {customer.contact_number}")
    
#     # Item List
#     y = height - 150
#     for item_name, quantity, price, amount in items_details:
#         p.drawString(100, y, f"{item_name} - Qty: {quantity}, Price: {price}, Amount: {amount}")
#         y -= 20
    
#     # Discounts and Totals
#     p.drawString(100, y, f"Discount: {discount_amount}")
#     y -= 20
#     p.drawString(100, y, f"Total Amount: {total_amount}")

#     p.showPage()
#     p.save()
#     return response




def create_pdf(worksite, customer, items_details, discount_amount, total_amount):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 28)
    p.drawString(200, height - 50, "Bill Estimate")
    
    # Underline the title
    p.setStrokeColor(colors.black)
    p.line(100, height - 60, 500, height - 60)
    
    p.setFont("Helvetica", 13)
    p.drawString(450, height - 80, f"Date: {timezone.now().strftime('%Y-%m-%d')}")
    
    # Subheading
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 100, "Quotation")
    
    p.setStrokeColor(colors.black)
    p.line(50, height - 110, 128, height - 110)


    # Customer Details
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 140, "Customer Details")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 160, f"Name: {customer.name}")
    p.drawString(50, height - 180, f"Location: {customer.location}")
    p.drawString(50, height - 200, f"Contact: {customer.contact_number}")


    # Table Header
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.darkblue)
    p.rect(50, height - 250, width - 100, 20, fill=1)  # Header background
    p.setFillColor(colors.white)
    p.drawString(60, height - 242, "Sl. No.")
    p.drawString(120, height - 242, "Item Name")
    p.drawString(300, height - 242, "Quantity")
    p.drawString(400, height - 242, "Rate")
    p.drawString(500, height - 242, "Amount")
    p.setFillColor(colors.black)

    # Item List
    y = height - 268
    p.setFont("Helvetica", 12)
    for idx, (item_name, quantity, price, amount) in enumerate(items_details, start=1):
        p.drawString(60, y, str(idx))
        p.drawString(120, y, item_name)
        p.drawString(300, y, str(quantity))
        p.drawString(400, y, f"{price:.2f}")
        p.drawString(500, y, f"{amount:.2f}")
        y -= 20

        # Check if we need to create a new page
        if y < 50:
            p.showPage()
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(colors.darkblue)
            p.rect(50, height - 210, width - 100, 20, fill=1)
            p.setFillColor(colors.white)
            p.drawString(60, height - 200, "Sl. No.")
            p.drawString(120, height - 200, "Item Name")
            p.drawString(300, height - 200, "Quantity")
            p.drawString(400, height - 200, "Price")
            p.drawString(500, height - 200, "Amount")
            p.setFillColor(colors.black)
            y = height - 230  # Reset y position for new page

    # Add borders around the table
    p.setStrokeColor(colors.black)
    p.rect(50, height - 230, width - 100, y - (height - 230), stroke=1, fill=0)

    # Discounts and Totals
    y -= 20  # Space before totals
    p.setFont("Helvetica-Bold", 14)
    p.drawString(120, y - 30, "Total Amount:")
    p.drawString(400, y - 30, f"{total_amount:.2f}")
    # p.drawString(200, y, f"Total Amount: {total_amount:.2f}")
    y -= 20
    if discount_amount > 0:
        p.setFont("Helvetica", 12)
        p.drawString(120, y - 30, "Discount: ")
        p.drawString(400, y - 30, f"{discount_amount:.2f}")
        y -= 20
    p.setFont("Helvetica-Bold", 14)
    p.drawString(120, y - 30, "Amount to be Paid: ")
    p.drawString(400, y - 30, f"{total_amount - discount_amount:.2f}")
    

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(100, 30, "This is a computer-generated document and does not require a signature.")

    # Finalize the PDF
    p.showPage()
    p.save()
    buffer.seek(0)  # Move to the beginning of the BytesIO buffer

    return buffer.read()  # Return the PDF data as bytes




def send_email_with_pdf(email, pdf_file):
    # Here you would implement the actual email sending logic with the PDF as an attachment.
    # For simplicity, this function is left unimplemented.
    send_mail(
        subject='Your Bill',
        message='Please find attached your bill.',
        from_email='your_email@example.com',
        recipient_list=[email],
        fail_silently=False,
    )




def purchase_input(request):
    
    work_id = request.GET.get('work_id')  # Get work_id from query parameters
    works = Work.objects.all()
    items = Item.objects.all()  # Get all items for the dropdown
    suppliers = Supplier.objects.all()  # Get all suppliers for the dropdown


    if request.method == 'POST':
        # Get data from the form
        work_id = request.POST.get('work')
        date = request.POST.get('date')
        invoice_number = request.POST.get('invoice_number')
        item_id = request.POST.get('item')
        quantity = request.POST.get('quantity')
        supplier_id = request.POST.get('supplier')
        amount = request.POST.get('amount')
        spent_by = request.POST.get('spent_by', 'Nivin')

        # Create purchase entry
        Purchase.objects.create(
            work_id=work_id,
            date=date,
            invoice_number=invoice_number,
            item_id=item_id,
            quantity=quantity,
            supplier_id=supplier_id,
            amount=amount,
            spent_by=spent_by,
        )
        
        item = Item.objects.get(id=item_id)
        item.stock_quantity += int(quantity)  # Increase stock by the quantity in the purchase
        item.save()
        
        
        return redirect('purchase_list')  # Redirect after saving

    # If GET request, render the input form
   
    return render(request, 'purchase_input.html', {'works': works, 'selected_work_id': work_id, 'items': items,
        'suppliers': suppliers})

def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'purchase_list.html', {'purchases': purchases})

def calculate_outstanding_balance(work_id):
    # Get the total received amount for the specified work
    total_received = Payment.objects.filter(work_id=work_id).aggregate(Sum('amount'))['amount__sum'] or 0

    # Get the total purchase for the specified work
    total_purchase = Purchase.objects.filter(work_id=work_id).aggregate(Sum('amount'))['amount__sum'] or 0

    # Find the outstanding balance
    return total_purchase - total_received


def view_updates(request, work_id):
    # Fetch the Work object using the provided work_id
    work = get_object_or_404(Work, id=work_id)

    # Get all updates related to the work
    updates = DailyUpdate.objects.filter(work=work).order_by('-date')  # Latest updates first

    # Render the page with the updates
    return render(request, 'view_updates.html', {
        'work': work,
        'updates': updates,
    })
    
    
    

# View for Group Chat

def group_chat(request):

    messages = GroupChatMessage.objects.all().order_by('timestamp')
    return render(request, 'group_chat.html', {'messages': messages})



def send_group_message(request):
    print(request.session.get('user_role'))
    if request.method == 'POST':
        
            sender_name = request.session.get('user_role')  # Get the name of the logged-in user
            message_text = request.POST.get('message')
            GroupChatMessage.objects.create(sender_name=sender_name, message=message_text)
            return redirect('group_chat')
    return redirect('login')




def worksite_details(request, worksite_id):
    worksite = get_object_or_404(Work, id=worksite_id)
    daily_updates = DailyUpdate.objects.filter(work=worksite)
    purchases = Purchase.objects.filter(work=worksite)
    payments = Payment.objects.filter(work=worksite)

    # Calculate total purchases for the worksite
    total_purchases = sum(purchase.amount for purchase in purchases)

    # Calculate total amount received from payments
    total_received = sum(payment.amount for payment in payments)

    # Determine outstanding payment
    total_amount = worksite.total_amount
    outstanding_payment = total_amount - total_received

    context = {
        'work': worksite,
        'daily_updates': daily_updates,
        'purchases': purchases,
        'payments': payments,
        'total_amount': total_amount,
        'total_purchases': total_purchases,
        'total_received': total_received,
        'outstanding_payment': outstanding_payment,
    }
    return render(request, 'worksite_details.html', context)



def item_allocation(request, work_id):
    print("1")
    work = get_object_or_404(Work, id=work_id)
    categories = Supplier.objects.values_list("category", flat=True).distinct()
    items = Item.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == 'POST':
        print("2")
        allocations = []
        index = 0

        while f'allocations_{index}_category' in request.POST:
            allocation = {
                'category': request.POST.get(f'allocations_{index}_category'),
                'item': request.POST.get(f'allocations_{index}_item'),
                'supplier': request.POST.get(f'allocations_{index}_supplier'),
                'quantity': request.POST.get(f'allocations_{index}_quantity')
            }
            allocations.append(allocation)
            index += 1

        print(allocations)  # Check if allocations is now populated

        for allocation in allocations:
            category = allocation['category']
            item_id = allocation['item']
            supplier_id = allocation['supplier']
            quantity = int(allocation['quantity'])

            # Continue with your logic here...
            # Check if the supplier provides the selected category
            supplier = Supplier.objects.get(id=supplier_id)
            if category not in supplier.category:
                print("3")
                messages.error(request, f"Supplier {supplier.name} does not provide items in the {category} category.")
                continue

            # Check stock quantity
            item = Item.objects.get(id=item_id)
            if quantity > item.stock_quantity:
                print("4")
                messages.error(request, f"Cannot allocate more than available stock for {item.name}.")
                continue

            # Create an allocation record
            ItemAllocation.objects.create(
                work=work,
                category=category,
                item_id=item_id,
                supplier_id=supplier_id,
                quantity_allocated=quantity
            )
            print("5")
            # Update stock quantity of the item
            item.stock_quantity -= quantity
            item.save()
        print("6")
        messages.success(request, "Items allocated successfully!")
        return redirect('allocation_list')

    print("7")
    return render(request, 'item_allocation.html', {
        'categories': categories,
        'items': items,
        'suppliers': suppliers
    })



# Function to display allocation list
def allocation_list(request):
    allocations = ItemAllocation.objects.select_related('work', 'item', 'supplier').all()
    return render(request, 'allocation_list.html', {'allocations': allocations})

# Function to fetch allocations by worksite ID (AJAX)
def get_allocations_by_work(request, work_id):
    allocations = ItemAllocation.objects.filter(work_id=work_id).select_related('item', 'supplier')
    data = [
        {
            'category': allocation.category,
            'item': allocation.item.name,
            'supplier': allocation.supplier.name,
            'quantity': allocation.quantity_allocated,
            'date_allocated': allocation.date_allocated.strftime('%Y-%m-%d %H:%M:%S')
        }
        for allocation in allocations
    ]
    return JsonResponse(data, safe=False)



def get_items_by_category(request, category):
    print("ok")
    items = Item.objects.filter(category=category).values('id', 'name')
    return JsonResponse(list(items), safe=False)

def get_suppliers_by_category_item(request, category, item_id):
    # Filter suppliers based on the category and item using the SupplierItem relationship
    suppliers = Supplier.objects.filter(
        category=category,
        supplieritem__item__id=item_id
    ).distinct().values('id', 'name')
    
    return JsonResponse(list(suppliers), safe=False)