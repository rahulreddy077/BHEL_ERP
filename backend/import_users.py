import os
import sys
import csv
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User

def import_users(csv_filepath):
    if not os.path.exists(csv_filepath):
        print(f"Error: File '{csv_filepath}' does not exist.")
        return
        
    print(f"Starting import from {csv_filepath}...")
    success_count = 0
    update_count = 0
    error_count = 0
    
    with open(csv_filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Verify columns
        required_cols = {'username', 'email', 'password', 'role', 'assigned_module'}
        if not required_cols.issubset(set(reader.fieldnames or [])):
            print(f"Error: CSV file must contain the following columns: {', '.join(required_cols)}")
            return
            
        for row in reader:
            username = row['username'].strip()
            email = row['email'].strip()
            password = row['password'].strip()
            role = row['role'].strip().upper()
            assigned_module = row['assigned_module'].strip().upper() or None
            
            # Normalize inputs
            if assigned_module == 'NONE' or assigned_module == '':
                assigned_module = None
                
            try:
                # Check if user already exists
                user, created = User.objects.get_or_create(username=username)
                
                user.email = email
                if password:
                    user.set_password(password) # automatically hashes
                user.role = role
                user.assigned_module = assigned_module
                
                # If SUPER_ADMIN, make them staff and superuser
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
                
                if created:
                    success_count += 1
                    print(f"Created user: {username} ({role})")
                else:
                    update_count += 1
                    print(f"Updated user: {username} ({role})")
            except Exception as e:
                error_count += 1
                print(f"Error importing user '{username}': {e}")
                
    print(f"\nImport Completed:")
    print(f"  - Created: {success_count}")
    print(f"  - Updated: {update_count}")
    print(f"  - Errors: {error_count}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python import_users.py <path_to_csv>")
        sys.exit(1)
        
    import_users(sys.argv[1])
