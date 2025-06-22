from nicegui import app

def set_jwt_cookie(token: str):
    app.storage.user['jwt'] = token

def get_jwt_token():
    return app.storage.user.get('jwt')

def clear_jwt_cookie():
    app.storage.user.pop('jwt', None)
