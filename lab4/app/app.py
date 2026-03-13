from flask import Flask
from flask_login import LoginManager
from models import db, User
from urls import register_urls
from flask_migrate import Migrate

app = Flask(__name__)
application = app

app.secret_key = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

    if not User.query.first():
        admin = User(
            login='admin',
            first_name='admin',
            last_name='admin',
            patronymic='admin'
        )
        admin.set_password('admin')

        db.session.add(admin)
        db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None

register_urls(app)

if __name__ == "__main__":
    app.run(debug=True)
