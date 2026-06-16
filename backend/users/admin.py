from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import csv
import io

class UserAdmin(DjangoUserAdmin):
    # Add custom fields to standard user list display
    list_display = DjangoUserAdmin.list_display + ('role', 'assigned_module')
    
    # Add custom fields to edit fieldsets
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('BHEL ERP Role & Access', {
            'fields': ('role', 'assigned_module'),
        }),
    )
    
    # Add custom fields to creation fieldsets
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('BHEL ERP Role & Access', {
            'fields': ('role', 'assigned_module'),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv_view), name='users_user_import_csv'),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if not csv_file or not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a valid CSV file.')
                return redirect('..')
            
            try:
                # Read file content safely
                data_set = csv_file.read().decode('utf-8')
                io_string = io.StringIO(data_set)
                reader = csv.DictReader(io_string)
                
                required_cols = {'username', 'email', 'password', 'role', 'assigned_module'}
                if not required_cols.issubset(set(reader.fieldnames or [])):
                    messages.error(request, f"CSV must contain headers: {', '.join(required_cols)}")
                    return redirect('..')
                
                success_count = 0
                error_count = 0
                
                for row in reader:
                    username = row['username'].strip()
                    email = row['email'].strip()
                    password = row['password'].strip()
                    role = row['role'].strip().upper()
                    assigned_module = row['assigned_module'].strip().upper() or None
                    
                    if assigned_module in ('NONE', '', 'NULL'):
                        assigned_module = None
                        
                    try:
                        user, created = User.objects.get_or_create(username=username)
                        user.email = email
                        if password:
                            user.set_password(password)
                        user.role = role
                        user.assigned_module = assigned_module
                        
                        if role == 'SUPER_ADMIN':
                            user.is_staff = True
                            user.is_superuser = True
                        elif role == 'MODULE_ADMIN':
                            user.is_staff = True
                            user.is_superuser = False
                        else:
                            user.is_staff = False
                            user.is_superuser = False
                            
                        user.save()
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                
                if error_count > 0:
                    messages.warning(request, f"Imported {success_count} users successfully. Failed to import {error_count} users due to errors.")
                else:
                    messages.success(request, f"Successfully imported {success_count} users from CSV.")
            except Exception as e:
                messages.error(request, f"Error processing CSV file: {e}")
                
            return redirect('..')
            
        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'title': 'Import Users from CSV',
        }
        return render(request, 'admin/users/user/import_csv.html', context)

admin.site.register(User, UserAdmin)