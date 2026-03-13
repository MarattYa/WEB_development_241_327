import random
from urllib.parse import urlparse
from flask import Flask, flash, redirect, render_template, request, make_response, session, url_for
from faker import Faker
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import re
import os

fake = Faker()

app = Flask(__name__)
application = app

os.urandom(30).hex()
app.secret_key=b'_5#y2Lz"F4Q8z\n\xec/'

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа необходимо авторизоваться'
login_manager.login_message_category = 'info'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {
    "user": {"password": "qwerty"}
}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None


def generate_comments(replies=True):
    comments = []
    for i in range(random.randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.text() }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'title': 'Заголовок поста',
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }

posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list)

@app.route('/posts/<int:index>')
def post(index):
    p = posts_list[index]
    return render_template('post.html', title=p['title'], post=p)

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

@app.route('/request-data')
def request_data():
    url_params = request.args.to_dict()
    
    headers = dict(request.headers)
    
    cookies = request.cookies
    
    return render_template('request_data.html', 
                         title='Данные запроса',
                         url_params=url_params,
                         headers=headers,
                         cookies=cookies)

@app.route('/set-cookie')
def set_cookie():
    resp = make_response(render_template('cookie_set.html'))
    resp.set_cookie('username', 'Marat')
    return resp 



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_page = request.args.get('next')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        next_page = request.form.get('next')

        if next_page in (None, '', 'None') or urlparse(next_page).netloc !='':
            next_page=None
        
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user, remember=remember)
            flash(f"Вы успешно вошли как {username}", "success")
            return redirect(next_page or url_for('index'))
        else:
            error = "Неверный логин или пароль"
            flash('Неверный логин или пароль', 'danger')

    return render_template('login.html', error=error, next_page=next_page)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

@app.route('/phone', methods=['GET','POST'])
def phone_check():
    error = None
    phone = ""
    formatted = None

    if request.method == 'POST':
        phone = request.form.get('phone','')

        allowed = re.fullmatch(r"[0-9+\-\s().]+", phone)

        if not allowed:
            error = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
        else:
            digits = re.sub(r"\D", "", phone)

            if phone.startswith("+7") or phone.startswith("8"):
                if len(digits) != 11:
                    error = "Недопустимый ввод. Неверное количество цифр."
            else:
                if len(digits) != 10:
                    error = "Недопустимый ввод. Неверное количество цифр."

            if not error:
                if len(digits) == 11:
                    digits = digits[1:]

                formatted = f"+7-{digits[0:3]}-{digits[3:6]}-{digits[6:8]}-{digits[8:10]}"

    return render_template(
        "check_phone.html",
        error=error,
        phone=phone,
        formatted=formatted
    )

@app.route('/visits_counter')
def visits():
    session['visit'] = session.get('visit',0) + 1 
    return render_template('visits_counter.html', visit = session['visit'])

if __name__ == "__main__":
    app.run(debug=True)
