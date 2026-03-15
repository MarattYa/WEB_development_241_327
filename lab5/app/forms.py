from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, EqualTo

class UserForm(FlaskForm):
    login = StringField('Логин', validators=[
        DataRequired(),
        Length(min=5),
        Regexp(r'^[A-Za-z0-9]+$', message="Только латинские буквы и цифры")    
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, max=128),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d~!?@#$%^&*_\-\+\(\)\[\]\{\}><\/\\|\"\'.,:;]+$',
               message="Пароль не соответствует требованиям")
    ])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[Optional(), Length(max=64)])
    role_id = SelectField('Роль', coerce=int)
    submit = SubmitField('Сохранить')

class UserEditForm(FlaskForm):

    first_name = StringField('Имя', validators=[
        DataRequired(message="Имя обязательно для заполнения"),
        Length(max=64, message="Имя не может быть длиннее 64 символов")
    ])
    last_name = StringField('Фамилия', validators=[
        Optional(),
        Length(max=64, message="Фамилия не может быть длиннее 64 символов")
    ])
    patronymic = StringField('Отчество', validators=[
        Optional(),
        Length(max=64, message="Отчество не может быть длиннее 64 символов")
    ])
    role_id = SelectField('Роль', coerce=int, choices=[], validators=[Optional()])
    submit = SubmitField('Сохранить')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[
        DataRequired(message="Введите старый пароль")
    ])
    
    new_password = PasswordField('Новый пароль', validators=[
        DataRequired(message="Введите новый пароль"),
        Length(min=8, max=128, message="Пароль должен быть от 8 до 128 символов"),
    ])
    
    confirm_password = PasswordField('Подтвердите новый пароль', validators=[
        DataRequired(message="Подтвердите новый пароль"),
        EqualTo('new_password', message="Пароли не совпадают")
    ])
    
    submit = SubmitField('Изменить пароль')


# Форма для логина
class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

# Форма для регистрации
class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[
        DataRequired(),
        Length(min=5),
        Regexp(r'^[A-Za-z0-9]+$', message="Только латинские буквы и цифры")
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8),
    ])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[Optional()])
    submit = SubmitField('Зарегистрироваться')