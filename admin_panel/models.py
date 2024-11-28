# models.py
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



# AdminCredentials Table
class AdminCredentials(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Consider using Django's password hashing for security
    email = models.EmailField()
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    

# Customer Table
class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    location = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Supplier Table
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Item Table
class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)  # New field for stock
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# SupplierItem Table (many-to-many relationship)
class SupplierItem(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} supplied by {self.supplier.name}"
    
# Enquiry Table (similar to Work table)
class Enquiry(models.Model):
    title = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    type_of_work = models.CharField(max_length=100)
    location = models.CharField(max_length=100)  # New field for enquiry location
    date_of_meeting = models.DateField()
    total_amount = models.IntegerField(default = 0)
    
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    
    status = models.CharField(max_length=20, choices=[
        ('unvisited', 'unvisited'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry for {self.customer.name} - {self.type_of_work}"

# Work Table 
class Work(models.Model):
    title = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    type_of_work = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('assigned', 'Assigned'),
        ('working', 'Working'),
        ('yet_to_start', 'Yet to Start'),
        ('completed', 'Completed')
    ])
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    action = models.TextField(null=True, blank=True)  # Remarks
    commitment = models.TextField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField(default = 0)

    def __str__(self):
        return f"Work for {self.customer.name} - {self.type_of_work}"


class FloorPlan(models.Model):
    work = models.ForeignKey(Work, related_name='floor_plans', on_delete=models.CASCADE)
    file = models.FileField(upload_to='floor_plans/')

class OtherDocument(models.Model):
    work = models.ForeignKey(Work, related_name='other_documents', on_delete=models.CASCADE)
    file = models.FileField(upload_to='other_documents/')


# Purchase Table
class Purchase(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    invoice_number = models.CharField(max_length=50)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent_by = models.CharField(max_length=100, default="Nivin")  # Name of payer
    purchase_bill = models.FileField(upload_to='purchase_bills/', null=True, blank=True)  # New field for purchase bill
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase for {self.work.description}"

# Account Table
class Account(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    balance_outstanding = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Account for {self.work.description}"

# Payment Table with signal to update Account balance
class Payment(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=100, choices=[
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash')
    ])
    reference_number = models.CharField(max_length=100, blank=True, default='N/A')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.work.description}: {self.amount}"

# Signal to update Account's balance_outstanding after a Payment is made
@receiver(post_save, sender=Payment)
def update_account_balance(sender, instance, **kwargs):
    try:
        account = Account.objects.get(work=instance.work)
        # Deduct payment amount from balance outstanding
        account.balance_outstanding -= instance.amount
        account.save()
    except Account.DoesNotExist:
        # Create an account record if it does not exist
        Account.objects.create(
            work=instance.work,
            date=timezone.now(),
            customer=instance.work.customer,
            amount=0,
            details="Auto-generated Account entry",
            balance_outstanding=-instance.amount
        )


# Employee Table
class Employee(models.Model):
    
    employee_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    department = models.TextField()
    username = models.CharField(max_length=150 )  # Add username field
    password = models.CharField(max_length=128)  # Add password field
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)  # New field
    pan_card_number = models.CharField(max_length=10, null=True, blank=True)  # New field
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)  # New field
    id_document = models.FileField(upload_to='employee_docs/', null=True, blank=True)  # New field
    
    
    def __str__(self):
        return f"{self.name} ({self.employee_code})"


class WorksiteAssignment(models.Model):
    worksite = models.ForeignKey('Work', on_delete=models.CASCADE, related_name='assignments')
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='assignments')
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} assigned to {self.worksite.title} on {self.date_assigned}"
    

class AdminMessage(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.employee} regarding {self.work} on {self.timestamp}"


class DailyUpdate(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)  # Foreign key to Work table
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Foreign key to Employee
    date = models.DateField(auto_now_add=True)
    update_text = models.TextField()
    work_image = models.ImageField(upload_to='daily_updates/')

    def __str__(self):
        return f"Update for {self.work} by {self.employee} on {self.date}"
    
# Group Chat Message Model
class GroupChatMessage(models.Model):
    sender_name = models.CharField(max_length=255)  # Stores the name of the sender
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender_name} at {self.timestamp}"
    
    
    
class ItemAllocation(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity_allocated = models.PositiveIntegerField()
    date_allocated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Allocation for {self.work.title} - {self.item.name} ({self.quantity_allocated})"