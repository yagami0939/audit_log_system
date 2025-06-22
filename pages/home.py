from nicegui import ui
from auth import decode_jwt_token
from utils import get_jwt_token, clear_jwt_cookie
from rbac import has_permission
from models.empolyee import Employee
from components.rich_table import build_table_ui
from components.rich_table_v2 import RichTable

def show():
    token = get_jwt_token()
    print("token",token)
    if not token:
        ui.navigate.to('/login')
        return

    payload = decode_jwt_token(token)
    print("paloady",payload)
    if not payload or not has_permission(payload['role'], 'home'):
        ui.notify('无权限访问', type='negative')
        ui.navigate.to('/login')
        return

    ui.label(f'欢迎你，用户ID: {payload["sub"]}, 角色: {payload["role"]}')

    # build_table_ui(Employee)
    RichTable(Employee)


    if payload['role'] == 'admin':
        ui.button('进入权限管理后台', on_click=lambda: ui.navigate.to('/admin'))
    ui.button('退出登录', on_click=lambda: (clear_jwt_cookie(), ui.navigate.to('/login')))
