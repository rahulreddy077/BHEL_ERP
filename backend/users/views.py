from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .permissions import has_module_access, can_edit

from engineering.models import EngineeringProject
from inventory.models import InventoryItem
from finance.models import FinanceTransaction
from apparatus.models import Apparatus
from technical.models import Document, TechnicalReport

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password."
            
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # Fetch real counts from the database
    metrics = {
        'projects_count': EngineeringProject.objects.count(),
        'inventory_count': InventoryItem.objects.count(),
        'finance_count': FinanceTransaction.objects.count(),
        'apparatus_count': Apparatus.objects.count(),
        'documents_count': Document.objects.count(),
    }
    return render(request, 'dashboard.html', {'metrics': metrics})

@login_required
def module_detail(request, module_name):
    # Normalize module name to uppercase to match model choices
    module_key = module_name.upper()
    
    # Check if user has access to this module
    if not has_module_access(request.user.role, request.user.assigned_module, module_key):
        return render(request, 'access_denied.html', {'module_name': module_name})
    
    # Check if user has edit permissions (for file upload form)
    user_can_edit = can_edit(request.user.role, request.user.assigned_module, module_key)
    
    error = None
    success_msg = None
    
    if request.method == 'POST' and user_can_edit:
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        uploaded_file = request.FILES.get('file')
        
        if title and uploaded_file:
            doc = Document.objects.create(
                title=title,
                description=description,
                module=module_key,
                uploaded_by=request.user.username,
                file=uploaded_file
            )
            success_msg = f"Document '{title}' uploaded successfully!"
        else:
            error = "Title and file are required fields."
            
    # Query documents related to this module
    documents = Document.objects.filter(module=module_key).order_by('-uploaded_at')
    
    # Render detail page
    context = {
        'module_name': module_name.title(),
        'module_key': module_key,
        'documents': documents,
        'user_can_edit': user_can_edit,
        'error': error,
        'success_msg': success_msg,
    }
    return render(request, 'module_detail.html', context)

@login_required
def finance_module(request):
    return module_detail(request, 'finance')