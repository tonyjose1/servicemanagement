from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.register_or_login, name='register_or_login'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get_upcoming_deadlines/', views.get_upcoming_deadlines, name='get_upcoming_deadlines'),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path('employee/manage/', views.manage_employees, name='manage_employees'),
    path('work/add/', views.add_work, name='add_worksite'),
    path('work/edit/<int:work_id>/', views.edit_work, name='edit_worksite'),
    path('work/delete/<int:work_id>/', views.delete_work, name='delete_worksite'),
    path('work/<int:work_id>/payments/', views.view_payments, name='view_payments'),
    path('work/<int:work_id>/payment/add/', views.add_payment, name='add_payment'),
    path('work/details/<int:work_id>/', views.work_details, name='work_details'),
    path('worksite-details/<int:worksite_id>/', views.worksite_details, name='worksite_details'),
    path('customer/add/', views.add_customer, name='add_customer'),
    path('supplier/add/', views.add_supplier, name='add_supplier'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('employees/details/<int:id>/', views.get_employee_details, name='get_employee_details'),
    path('employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path('manage-assignments/', views.manage_assignments, name='manage_assignments'),
    path('manage-assignments/worksite/<int:worksite_id>/', views.get_worksite_assignments, name='get_worksite_assignments'),
    path('manage-assignments/employee/<int:employee_id>/', views.get_employee_assignments, name='get_employee_assignments'),
    path("suppliers/add/", views.add_supplier, name="add_supplier"),
    path("suppliers/", views.view_suppliers, name="view_suppliers"),
    path("suppliers/edit/<int:supplier_id>/", views.edit_supplier, name="edit_supplier"),
    path("suppliers/delete/<int:supplier_id>/", views.delete_supplier, name="delete_supplier"),
    path("suppliers/view/<int:supplier_id>/", views.view_supplier_details, name="view_supplier_details"),
    path("items/add/", views.add_item, name="add_item"),
    path("items/", views.view_items, name="view_items"),
    path("items/edit/<int:item_id>/", views.edit_item, name="edit_item"),
    path("items/delete/<int:item_id>/", views.delete_item, name="delete_item"),
    path("items/view/<int:item_id>/", views.view_item_details, name="view_item_details"),
    path("get-suppliers/", views.get_suppliers, name="get_suppliers"),
    path('generate_bill/<int:worksite_id>/', views.generate_bill, name='generate_bill'),
    path('submit_bill/', views.submit_bill, name='submit_bill'),
    path('purchase/input/', views.purchase_input, name='purchase_input'),
    path('purchase/list/', views.purchase_list, name='purchase_list'),
    path('worksite/<int:work_id>/updates/', views.view_updates, name='view_updates'),
    path('group-chat/', views.group_chat, name='group_chat'),
    path('send-group-message/', views.send_group_message, name='send_group_message'),
    path('item_allocation/', views.item_allocation, name='item_allocation'),
    path('allocation_list/', views.allocation_list, name='allocation_list'),
    path('get_allocations_by_work/<int:work_id>/', views.get_allocations_by_work, name='get_allocations_by_work'),
    path('item_allocation/<int:work_id>/', views.item_allocation, name='item_allocation'),
    path('get-items/<str:category>/', views.get_items_by_category, name='get_items_by_category'),
    path('get-suppliers/<str:category>/<int:item_id>/', views.get_suppliers_by_category_item, name='get_suppliers_by_category_item'),
    
        
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)