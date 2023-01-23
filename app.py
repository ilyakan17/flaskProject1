from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laba.db'
db = SQLAlchemy(app)
app.secret_key = '12341234i'

class users(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    check_password = db.Column(db.Text, nullable=False)


class products(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    type = db.Column(db.String, nullable=False)
    namep = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    brand = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']
        check_password = request.form['check_password']

        Users = users(email=email, login=login, password=password, check_password=check_password)
        try:
            db.session.add(Users)
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка("
    else:
        return render_template("/index.html")


@app.route('/authentication', methods=["GET", "POST"])
def authentication():
    result1 = "Введите логин и пароль"
    if request.method == "POST":

        login = request.form.get("login")
        password = request.form.get("password")

        user_test = users.query.filter_by(login=login).first()
        if user_test is None:
            result1 = 'Пользователя с таким логином и паролем не существует'
        elif user_test.password != password:
            result1 = 'Введён неверный пароль'
        else:
            result1 = 'Мы нашли вас'
            if login != 'admin':
                session["user"] = login
                return redirect(url_for('create_user'))
            if login == 'admin':
                session["admin"] = login
                return redirect('admin')

    return render_template("auth.html", result1=result1)

@app.route('/admin', methods=["GET", "POST"])
def admin():
    return render_template("admin.html")

@app.route('/add_product', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        type = request.form['type']
        namep = request.form['namep']
        description = request.form['description']
        brand = request.form['brand']
        price = request.form['price']
        photo = request.form['photo']

        Products = products(type=type, namep=namep, description=description, brand=brand, price=price, photo=photo)
        try:
            db.session.add(Products)
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка("
    return render_template("add.html")

@app.route('/admin/delete/', methods=['GET', 'POST'])
def admin_delete():
    if "admin" in session:
        add_result = ''
        if request.method == 'POST':
            namep = request.form["namep"]
            if namep == "":
                add_result = 'Неправильное название товара'
            else:
                product = products(namep=request.form["namep"])
                product_test_name = products.query.filter_by(namep=product.namep).first()
                if product_test_name is None:
                    add_result = 'Такой товар не найден'
                    return render_template('/delete.html', add_result=add_result)
                else:
                    db.engine.execute(f"DELETE FROM products WHERE namep = '{namep}'")
                    add_result = 'Товар удалён успешно!'
        return render_template('/delete.html', add_result=add_result)
    else:
        return redirect(url_for('authentication'))

@app.route('/card', methods=["GET", "POST"])
def card_product():
    cards = products.query.order_by(products.price).all()
    return render_template("cards.html", cards=cards)

@app.route('/list', methods=["GET", "POST"])
def list():
    lists = products.query.all()
    return render_template("list.html", lists=lists)

if __name__ == '__main__':
    app.run(debug=True)
