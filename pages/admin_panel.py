from nicegui import ui
from auth import decode_jwt_token
from utils import get_jwt_token
from rbac import has_permission
from database import SessionLocal
from models.user import User

def show():
    token = get_jwt_token()
    if not token:
        ui.navigate.to('/login')
        return

    payload = decode_jwt_token(token)
    if not payload or not has_permission(payload['role'], 'admin_panel'):
        ui.notify('无权限访问', type='negative')
        ui.navigate.to('/')
        return

    db = SessionLocal()
    users = db.query(User).all()

    ui.label('用户权限管理后台').classes('text-2xl mt-4')
    columns=[
            {'name': 'id', 'label': 'ID', 'field': 'id'},
            {'name': 'username', 'label': '用户名', 'field': 'username'},
            {'name': 'role', 'label': '角色', 'field': 'role'},
            {'name': 'action', 'label': '操作'},
        ]
    # 准备数据行
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'username': user.username,
            'role': user.role,
        })

    def template(row):
            ui.label(str(row['id']))
            ui.label(row['username'])

            role_select = ui.select(
                ['admin', 'editor', 'viewer'],
                value=row['role'],
                dense=True,
            ).props('outlined dense')

            def update_role():
                session = SessionLocal()
                db_user = session.query(User).filter(User.id == row['id']).first()
                if db_user:
                    db_user.role = role_select.value
                    session.commit()
                    ui.notify(f"{db_user.username} 的角色已更新为 {db_user.role}", type='positive')
                session.close()

            ui.button('更新角色', on_click=update_role).props('dense')
    # 构建表格
    table = ui.table(columns =columns, rows=data, row_key='id').classes('w-full')
    # table.row_template(template)
        

    db.close()

    ui.button('返回主页', on_click=lambda: ui.navigate.to('/')).classes('mt-4')
