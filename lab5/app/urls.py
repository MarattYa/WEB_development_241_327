
from views import index, login, logout, users_list, user_create, user_edit, delete_user, profile, edit_profile, change_password,user_view,register

def register_urls(app):
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/auth/register','register',register,methods=['GET','POST'])
    app.add_url_rule('/auth/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)

    app.add_url_rule('/users', 'users_list', users_list)
    app.add_url_rule('/users/create', 'user_create', user_create, methods=['GET', 'POST'])
    app.add_url_rule('/users/<int:id>/edit', 'user_edit', user_edit, methods=['GET', 'POST'])
    app.add_url_rule('/users/<int:user_id>/delete', 'delete_user', delete_user, methods=['POST'])
    app.add_url_rule('/users/<int:id>', 'user_view', user_view)

    app.add_url_rule('/profile', 'profile', profile)
    app.add_url_rule('/profile/edit', 'edit_profile', edit_profile, methods=['GET', 'POST'])
    app.add_url_rule('/change-password', 'change_password', change_password, methods=['GET', 'POST'])