from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    users = db.relationship('User', back_populates='role', lazy='dynamic')

    @staticmethod
    def create_default_roles():
        roles = {
            'Администратор': 'Полный доступ к системе',
            'Пользователь': 'Ограниченный доступ'
        }
        for role_name, role_desc in roles.items():
            if not Role.query.filter_by(name=role_name).first():
                role = Role(name=role_name, description=role_desc)
                db.session.add(role)
        db.session.commit()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64), nullable=False)
    patronymic = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)

    role = db.relationship('Role', back_populates='users')
    visits = db.relationship('VisitLog', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return " ".join(filter(None, [self.last_name, self.first_name, self.patronymic]))

    @property
    def is_admin(self):
        return self.role and self.role.name == 'Администратор'


class VisitLog(db.Model):
    __tablename__ = 'visit_logs'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='visits')
    
    def __repr__(self):
        return f"<VisitLog {self.path} by {self.user_id} at {self.created_at}>"