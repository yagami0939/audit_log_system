role_permissions = {
    'admin': ['home', 'admin_panel'],
    'editor': ['home'],
    'viewer': ['home'],
}

def has_permission(role: str, page: str):
    return page in role_permissions.get(role, [])
