def has_module_access(user_role, user_module, requested_module):

    if user_role == 'SUPER_ADMIN':
        return True

    elif user_role == 'MODULE_ADMIN':
        return user_module == requested_module

    elif user_role == 'USER':
        return user_module == requested_module

    return False


def can_edit(user_role, user_module, requested_module):

    if user_role == 'SUPER_ADMIN':
        return True

    elif user_role == 'MODULE_ADMIN':
        return user_module == requested_module

    return False