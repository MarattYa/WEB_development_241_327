from sqlite3 import IntegrityError
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from decorators import check_rights
from models import VisitLog, db, User, Role
from forms import ChangePasswordForm, UserEditForm, UserForm
from sqlalchemy import func


def index():
    return render_template("index.html")


def login():
    if request.method == 'POST':
        login_name = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(login=login_name).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Вы успешно вошли в систему!",'success')
            return redirect(url_for('index'))
        else:
            flash("Неверный логин или пароль", 'danger')

    return render_template("auth/login.html")


@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", 'success')
    return redirect(url_for('index'))


@login_required
@check_rights(['Администратор'])
def users_list():
    users = User.query.all()
    return render_template("users/index.html", users=users)


@login_required
@check_rights(['Администратор'])
def user_view(id):
    user = User.query.get_or_404(id)
    return render_template("users/view.html", user=user)


@login_required
@check_rights(['Администратор'])
def user_create():
    form = UserForm()
    roles = Role.query.filter(Role.name != "Администратор").all()
    form.role_id.choices = [(0, 'Без роли')] + [(r.id, r.name) for r in roles]

    if form.validate_on_submit():
        try:
            user = User(
                login=form.login.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                role_id=form.role_id.data if form.role_id.data != 0 else None
            )

            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            flash(f'Пользователь {user.full_name} успешно создан', 'success')
            return redirect(url_for('users_list'))

        except IntegrityError:
            db.session.rollback()
            flash('Пользователь с таким логином уже существует', 'danger')

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании пользователя: {str(e)}', 'danger')

    return render_template("users/create.html", form=form)


@login_required
@check_rights(['Администратор'])
def user_edit(id):
    user = User.query.get_or_404(id)

    form = UserEditForm(obj=user)
    form.role_id.choices = [(0, 'Без роли')] + [(r.id, r.name) for r in Role.query.all()]

    if current_user.role.name == 'Пользователь':
        form.role_id.render_kw = {'disabled': True}

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        if current_user.role.name == 'Администратор':
            user.role_id = form.role_id.data or None

        db.session.commit()

        flash(f'Данные пользователя {user.full_name} обновлены', 'success')
        return redirect(url_for('users_list'))

    return render_template("users/edit.html", form=form, user=user)


@login_required
@check_rights(['Администратор'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        flash("Пользователь удалён", "success")

    except:
        db.session.rollback()
        flash("Ошибка удаления", "danger")

    return redirect(url_for('users_list'))


@login_required
def profile():
    return render_template("profile/profile.html")


@login_required
def edit_profile():

    user = current_user
    form = UserEditForm(obj=user)

    form.role_id.choices = []
    form.role_id.render_kw = {'disabled': True}

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.patronymic = form.patronymic.data

        db.session.commit()

        flash("Данные профиля обновлены", "success")
        return redirect(url_for('profile'))

    return render_template("profile/edit_profile.html", form=form)


@login_required
def change_password():

    form = ChangePasswordForm()

    if form.validate_on_submit():

        if current_user.check_password(form.old_password.data):

            current_user.set_password(form.new_password.data)
            db.session.commit()

            flash('Пароль успешно изменен', 'success')
            return redirect(url_for('profile'))

        else:
            flash('Неверный старый пароль', 'danger')

    return render_template("profile/change_password.html", form=form)



def register():

    if request.method == 'POST':

        login_name = request.form.get('login')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        patronymic = request.form.get('patronymic')

        if User.query.filter_by(login=login_name).first():
            flash("Пользователь с таким логином уже существует", "danger")
            return  redirect(url_for('auth/register'))

        user_role = Role.query.filter_by(name="Пользователь").first()

        user = User(
            login=login_name,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            role=user_role
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Регистрация прошла успешно! Теперь можно войти.", "success")

        return redirect(url_for('login'))

    return render_template("auth/register.html")