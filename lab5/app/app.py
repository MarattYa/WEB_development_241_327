from flask import Flask, request
from flask_login import LoginManager, current_user
from models import db, User, Role, VisitLog
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    Role.create_default_roles()
    if not User.query.first():
        admin_role = Role.query.filter_by(name='Администратор').first()
        admin = User(login='admin', first_name='admin', last_name='admin', patronymic='admin', role=admin_role)
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from urls import register_urls
register_urls(app)

from reports import reports
app.register_blueprint(reports)

@app.before_request
def log_visit():
    if request.endpoint == 'static':
        return
    user_id = current_user.id if current_user.is_authenticated else None
    db.session.add(VisitLog(path=request.path, user_id=user_id))
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)