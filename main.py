from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mail import Mail, Message
from sqlalchemy.exc import IntegrityError
import hashlib
import os
from models import db, User, Pet
from api import api_bp

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = 'bc72183212182182171232192137ab98798799869ffa9q6969fa69f69v8s9'
app.config["JSON_AS_ASCII"] = True
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('mail')
app.config['MAIL_PASSWORD'] = os.environ.get('password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('mail')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'instance', 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail(app)
db.init_app(app)

app.register_blueprint(api_bp, url_prefix="/api")


def create_user_session(user_id, username, email, is_admin):
    session['user_id'] = user_id
    session['username'] = username
    session['email'] = email
    session['is_admin'] = is_admin


def get_current_user():
    user_id = session.get('user_id')
    return User.query.get(user_id) if user_id else None


def create_pet(name, image, description, age, pet_type):
    new_pet = Pet(name=name, image=image, description=description, age=age, pet_type=pet_type)
    db.session.add(new_pet)
    db.session.commit()


def get_all_pets():
    return Pet.query.all()


def get_filtered_pets(pet_type_filter):
    if pet_type_filter:
        return Pet.query.filter_by(pet_type=pet_type_filter).all()
    else:
        return get_all_pets()


def delete_pet(pet_id):
    pet = Pet.query.filter(Pet.id == pet_id).first()
    if pet:
        db.session.delete(pet)
        db.session.commit()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.email and hashlib.sha224(password.encode()).hexdigest() == user.password:
            create_user_session(user.id, user.username, user.email, user.is_admin)
            flash('Успешная авторизация!', 'success')
            return redirect('/')
        else:
            flash('Неверный логин или пароль', 'error')
            return redirect('/sign_in')

    return render_template("sign_in.html")


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_admin = bool(request.form.get('is_admin'))

        if not email or '@' not in email:
            flash('Некорректный email', 'error')
            return render_template('sign_up.html', invalid_email=True)

        password_hash = hashlib.sha224(password.encode()).hexdigest()

        try:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Такой пользователь уже существует', 'error')
                return redirect('/sign_in')

            new_user = User(username=username, email=email, password=password_hash, is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            create_user_session(new_user.id, new_user.username, new_user.email, new_user.is_admin)
            flash('Регистрация прошла успешно!', 'success')
            return redirect('/')

        except IntegrityError:
            db.session.rollback()
            flash('Ошибка при регистрации', 'error')

    return render_template('sign_up.html')


@app.route('/sign_out')
def sign_out():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('is_admin', None)
    flash('Вы успешно вышли', 'success')
    return redirect('/')


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        pet_type_filter = request.form.get('pet_type')
        pets = get_filtered_pets(pet_type_filter)
    else:
        pets = get_all_pets()

    pet_data = [{"name": pet.name, "image": pet.image} for pet in pets]
    return render_template("articles.html", pets=pet_data)


@app.route('/article/<name>')
def article(name):
    pet = Pet.query.filter_by(name=name).first()
    if pet:
        return render_template("article.html", pet_name=pet.name, pet_image=pet.image, pet_description=pet.description)
    else:
        return "Питомец не найден", 404


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        msg = Message("Вам поступило новое обращение на сайте", recipients=[name])
        msg.body = f"Клиент оставил номер телефона: {phone} и сообщение: {message}"
        mail.send(msg)
        flash('Сообщение отправлено', 'success')
        return redirect(url_for("contact"))
    return render_template("contact.html")


@app.route('/profile')
def profile():
    user = get_current_user()
    if user:
        return render_template('prof.html', user=user)
    else:
        return redirect('/sign_in')


@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    user = get_current_user()
    if user and user.is_admin:
        if request.method == 'POST':
            if 'add_pet' in request.form:
                name = request.form.get('name')
                image = request.form.get('image')
                description = request.form.get('description')
                age = request.form.get('age')
                pet_type = request.form.get('pet_type')

                create_pet(name, image, description, age, pet_type)
                flash('Питомец успешно добавлен', 'success')

            elif 'delete_pet' in request.form:
                pet_id = request.form.get('pet_id')
                delete_pet(pet_id)
                flash('Питомец успешно удален', 'success')

        pets = get_all_pets()
        return render_template('admin_panel.html', pets=pets)
    else:
        flash('У вас нет прав доступа к админ-панели', 'error')
        return redirect('/')


@app.route('/pets_list')
def pets_list():
    user = get_current_user()
    if user and user.is_admin:
        pets = get_all_pets()
        return render_template('pets_list.html', pets=pets)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
