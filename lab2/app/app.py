import random
from flask import Flask, render_template, request, make_response
from faker import Faker
import re

fake = Faker()

app = Flask(__name__)
application = app

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

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
    login_data = None
    if request.method == 'POST':
        login_data = {
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'remember': request.form.get('remember') == 'on'
        }
    return render_template('login.html', 
                         title='Авторизация',
                         login_data=login_data)

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
if __name__ == "__main__":
    app.run(debug=True)
