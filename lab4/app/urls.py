from views import *

def register_urls(app):
    app.add_url_rule('/', 'index', index)
    
    app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)
    
    app.add_url_rule('/users', 'users_list', users_list)
    app.add_url_rule('/users/<int:id>', 'user_view', user_view)
    
    app.add_url_rule('/users/create', 'user_create', user_create, methods=['GET', 'POST'])
    app.add_url_rule('/users/<int:id>/edit', 'user_edit', user_edit, methods=['GET', 'POST'])
    app.add_url_rule('/users/<int:user_id>/delete', 'user_delete', delete_user, methods=['POST'])
    
    app.add_url_rule('/change-password', 'change_password', change_password, methods=['GET', 'POST'])