from flask import Flask, render_template, url_for, request, flash, redirect, session, abort
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b6d5c229fb79b9317978f4550749edfdc0bc66b3'
app.permanent_session_lifetime = datetime.timedelta(days=10)

menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]


@app.route("/index")
@app.route("/")
def index():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template('index.html', title="Про Flask", menu=menu)


data = [1, 2, 3, 4]


@app.route("/session")
def session_data():
    session.permanent = True
    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][1] += 1
        session.modified = True
    return f"session['data']: {session['data']}"


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)  # ошибка доступа, прерывание
    return f"Пользователь: {username}"


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Mistake', category='error')
    return render_template('contact.html', title="Обратная связь", menu=menu)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'znam' and request.form['psw'] == '1234':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=menu)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Page not found', menu=menu), 404


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username="selfedu"))

if __name__ == '__main__':
    app.run(debug=True)
