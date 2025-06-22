from nicegui import ui
from database import Base, engine
import pages.login as login
import pages.register as register
import pages.home as home
import pages.admin_panel as admin_panel

# 初始化数据库结构
Base.metadata.create_all(bind=engine)

@ui.page('/')
def index():
    home.show()

@ui.page('/login')
def login_page():
    login.show()

@ui.page('/register')
def register_page():
    register.show()

@ui.page('/admin')
def admin_page():
    admin_panel.show()

ui.run(title='NiceGUI 登录系统', storage_secret='supersecret',reload=True)
