import flask
from flask import Flask, render_template
from flask import url_for
from flask import request, redirect, make_response
from db import give_price, check_login, check_in_db, add_to_db
from db import add_new_user, new_product, add_money, get_money
from db import add_everyone_0, add_1_to_own, my_thing, give_am
from db import all_products, get_user_name
import os
import cv2
from model import model_pred

mon = {'arnault': 238.4, 'bezos': 132.8, 'billy': 1000.0, 'bill_gates': 111.8, 'brin': 88.6, 'buffit': 114.6,
       'buterin': 0.9264, 'chan': 0.5, 'cruise': 1.2, 'durov': 11.5, 'dwayne_jonson': 0.8, 'ellish': 69.0,
       'ellon_musk': 171.8, 'franconise': 95.5, 'friedkin': 5.5, 'gosling': 300.0, 'jay_z': 1.0, 'koch': 59.0,
       'larry_page': 92.5, 'quandt': 25.7, 'reevs': 77.0, 'rihanna': 1.0, 'sandleer': 3.0, 'schwarzengger': 306.0,
       'scott': 0.001, 'spielberg': 3.0, 'stallone': 10.0, 'travis': 0.0001, 'west': 0.4, 'zuckerberg': 84.9}
app = Flask(__name__, template_folder=r'html_css',
            static_folder=r'html_css/css')
current_user = ''
app.config['UPLOAD_FOLDER'] = 'html_css/css/images'


@app.route('/', methods=['GET', 'POST'])
def home():
    if check_in_db(request.cookies.get('usermoti4k123')):
        return redirect('/shop')
    else:
        return redirect('/login')


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if check_in_db(request.cookies.get('usermoti4k123')):
        money = get_money(request.cookies.get('usermoti4k123'))
        if request.method == "POST":
            try:
                if 'btn' in request.form:
                    a = request.form['btn']
                else:
                    a = ''
                a = request.form['btn']
                if a == "Add products":
                    return redirect("/add_things")
                if a == "My things":
                    return redirect("/my_things")
                elif a == "Take photo":
                    return redirect('/photo')
                elif a == "Profile":
                    return redirect('/login')
                elif len(a) >= 5:
                    if money - give_price(a[4:].capitalize()) >= 0 and money - give_price(a[4:]) >= 0:
                        if give_price(a[4:].capitalize()) == 0:
                            money -= give_price(a[4:])
                        else:
                            money -= give_price(a[4:].capitalize())
                        us = get_user_name(a[4:])
                        m = give_price(a[4:])
                        add_money(us, m + get_money(us))
                        add_money(request.cookies.get('usermoti4k123'), money)
                        add_1_to_own(request.cookies.get('usermoti4k123'), a[4:])
                res = make_response(
                    render_template('buy_smth.html', set_scroll=a,
                                    money=str(get_money(request.cookies.get('usermoti4k123')))))
                return res
            except Exception:
                pass
        else:
            return render_template('buy_smth.html', money=str(money))
    else:
        return redirect('/login')


@app.route('/photo', methods=['GET', 'POST'])
def photo():
    global mon
    if check_in_db(request.cookies.get('usermoti4k123')):
        if request.method == "POST":
            try:
                if 'btn' in request.form:
                    a = request.form['btn']
                    if a == "Shop":
                        return redirect("/shop")
                    elif a == "Add products":
                        return redirect("/add_things")
                    if a == "My things":
                        return redirect("/my_things")
                    elif a == "Profile":
                        return redirect('/login')
                else:
                    file = request.files['photo']
                    user = request.cookies.get('usermoti4k123')
                    filename = file.filename
                    a = filename.find('.')
                    f = user + filename[a:]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], f))
                    a = model_pred(app.config['UPLOAD_FOLDER'] + "/" + f)
                    add_money(user, int(mon[a[0]] * 100000000))
                    add_everyone_0()
                    return render_template('photo.html', image=a[1], person=a[0], image2=r"css/images" + "/" + f,
                                           money=int(mon[a[0]] * 10000000))
            except Exception:
                pass
        else:
            return render_template('photo.html')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == "POST":
        try:
            user = request.form['nickname']
            user = user.strip()
            email = request.form['email']
            email = email.strip()
            password = request.form['password']
            password = password.strip()
            if check_login(user, password, email):
                current_user = user
                money = get_money(user)
                add_everyone_0()
                res = make_response(redirect('/shop'))
                res.set_cookie('usermoti4k123', user, max_age=None)
                return res
            else:
                return render_template('registration.html')
        except Exception:
            pass
    else:
        return render_template('registration.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        try:
            user = request.form['nickname']
            user = user.strip()
            email = request.form['email']
            email = email.strip()
            password = request.form['password']
            password = password.strip()
            add_new_user(user, password, email)
            add_money(user, 0)
            money = get_money(user)
            add_everyone_0()
            res = make_response(redirect('/shop'))
            res.set_cookie('usermoti4k123', user, max_age=None)
            return res
        except Exception:
            pass
    else:
        return render_template('signup.html')


@app.route('/add_things', methods=['GET', 'POST'])
def add_things():
    if check_in_db(request.cookies.get('usermoti4k123')):
        if request.method == "POST":
            try:
                if 'btn' in request.form:
                    a = request.form['btn']
                else:
                    a = ''
                if a == "Shop":
                    return redirect("/shop")
                elif a == "Take photo":
                    return redirect('/photo')
                elif a == "Profile":
                    return redirect('/login')
                elif a == "My things":
                    return redirect("/my_things")
                name = request.form['name']
                name = name.strip()
                if name == '':
                    name = '_'
                h = name
                name = ''
                for i in h:
                    if i != "'" and i not in '""':
                        name += i
                if name not in all_products():
                    price = int(request.form['price'])
                    file = request.files['photo']
                    user = request.cookies.get('usermoti4k123')
                    filename = file.filename
                    a = filename.find('.')
                    f = name + filename[a:]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], f))
                    new_product(name, price, user, f)
                    my_thing(name, price, user, f)
                    add_to_db(name, price, user)
                    add_everyone_0()
                return render_template('add_things.html')
            except Exception:
                pass
        else:
            return render_template('add_things.html')
    else:
        return redirect('/login')


@app.route('/my_things', methods=['GET', 'POST'])
def my_things():
    if check_in_db(request.cookies.get('usermoti4k123')):
        add_everyone_0()
        user = request.cookies.get('usermoti4k123')
        if request.method == "POST":
            try:
                a = request.form['btn']
                if a == "Shop":
                    return redirect("/shop")
                if a == "Add products":
                    return redirect("/add_things")
                elif a == "Take photo":
                    return redirect('/photo')
                elif a == "Profile":
                    return redirect('/login')
            except Exception:
                pass
        else:
            products = all_products()
            params = {}
            for i in products:
                u = i.replace(' ', '_')
                u = u.replace('.', "_")
                params[u] = give_am(user, i)
            return render_template("my_things.html", user=user.upper(), **params)
    else:
        return redirect("/login")


# buysellrepeat.fun
if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)
