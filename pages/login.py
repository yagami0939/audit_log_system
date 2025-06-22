from nicegui import ui
from auth import verify_user, create_jwt_token
from captcha_utils import generate_captcha
from io import BytesIO
import base64
from utils import *

captcha_text = None

def show():
    global captcha_text
    ui.label('用户登录').classes('text-2xl text-center')

    with ui.card().classes('w-80 mx-auto'):
        username = ui.input('用户名')
        password = ui.input('密码', password=True)
        captcha_input = ui.input('验证码')

        def refresh_captcha():
            global captcha_text
            captcha_text, image_data = generate_captcha()
            b64 = base64.b64encode(image_data.read()).decode()
            captcha_img.set_source(f'data:image/png;base64,{b64}')

        captcha_img = ui.image().classes('w-full h-16 cursor-pointer')
        captcha_img.on('click', lambda e: refresh_captcha())
        refresh_captcha()

        def handle_login():
            if captcha_input.value.upper() != captcha_text.upper():
                ui.notify('验证码错误', type='negative')
                refresh_captcha()
                return
            user = verify_user(username.value, password.value)
            if user:
                token = create_jwt_token(user.id, user.role)
                set_jwt_cookie(token)
                ui.navigate.to('/')
            else:
                ui.notify('用户名或密码错误', type='negative')

        ui.button('登录', on_click=handle_login).classes('w-full')
        ui.button('注册', on_click=lambda: ui.navigate.to('/register')).classes('w-full mt-2')

