from nicegui import ui
from auth import register_user

def show():
    ui.label('注册用户').classes('text-2xl text-center')

    with ui.card().classes('w-80 mx-auto'):
        username = ui.input('用户名')
        password = ui.input('密码', password=True)

        def handle_register():
            if register_user(username.value, password.value):
                ui.notify('注册成功，请登录', type='positive')
                ui.navigate('/login')
            else:
                ui.notify('用户名已存在', type='warning')

        ui.button('注册', on_click=handle_register).classes('w-full')
        ui.button('返回登录', on_click=lambda: ui.navigate('/login')).classes('w-full mt-2')
