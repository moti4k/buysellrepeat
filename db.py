import sqlite3


def give_price(name):
    # Подключение к БД
    con = sqlite3.connect("db/products.db")

    # Создание курсора
    cur = con.cursor()

    # Выполнение запроса и получение всех результатов
    result = cur.execute(f"""SELECT price FROM
     products WHERE name = '{name}'""").fetchall()
    con.close()
    try:
        return result[0][0]
    except Exception:
        return 0


def check_login(nickname, password, email):
    # Подключение к БД
    con = sqlite3.connect("db/products.db")

    # Создание курсора
    cur = con.cursor()

    # Выполнение запроса и получение всех результатов
    result = cur.execute(f"""SELECT nickname, password, email FROM
     user WHERE nickname='{nickname}' and password='{password}' and email='{email}'""").fetchall()
    con.close()
    if len(result) > 0:
        return True
    else:
        return False


def check_in_db(user):
    con = sqlite3.connect("db/products.db")

    # Создание курсора
    cur = con.cursor()

    # Выполнение запроса и получение всех результатов
    result = cur.execute(f"""select email from user where nickname='{user}'""").fetchall()
    if result:
        return True
    return False


def add_to_db(name, price, user):
    # Подключение к БД
    con = sqlite3.connect("db/products.db")

    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    result = cur.execute(f"""INSERT INTO products(user, name, price) VALUES('{user}', '{name}', {price})""")
    con.commit()
    con.close()


def add_everyone_0():
    con = sqlite3.connect("db/products.db")

    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    result = cur.execute(f"""Select nickname from user""").fetchall()
    users = tuple(map(lambda x: x[0], result))
    result2 = cur.execute(f"""Select name, price from products""").fetchall()
    check = cur.execute(f"""Select name, user from own""").fetchall()
    for i in users:
        for product in result2:
            flag = True
            for non in check:
                if non == (product[0], i):
                    flag = False
                    break
            if flag:
                add = cur.execute(
                    f"""INSERT INTO own(name, user, amount, price) VALUES('{product[0]}', '{i}', 0, {product[1]})""")
                con.commit()
    con.close()


def add_1_to_own(user, name):
    con = sqlite3.connect("db/products.db")

    # Создание курсора
    cur = con.cursor()
    add = cur.execute(f"""Update own SET amount = amount + 1
        WHERE user = '{user}' and name='{name}'""")
    con.commit()
    con.close()


import sqlite3


def add_new_user(nickname, password, email):
    # Подключение к БД
    con = sqlite3.connect("db/products.db")
    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    result = cur.execute(
        f"""INSERT INTO user(nickname, password, email) VALUES('{nickname}', '{password}', '{email}')""")
    con.commit()
    con.close()


def new_product(name, price, user, filename):
    file = open('html_css/buy_smth.html', mode='r', encoding='utf-8')
    u = file.read()
    file.close()
    data = u
    img = data.count('img')
    print(data)
    a = f"""<div class="product_name">
                <p class="txt" id="Buy_{name}">{name}: {price}RUB <span class="user">by {user}</span></p>
                <img class="photo" src="css/images/{filename}">
                <input type="submit" class="buy" name="btn" value="Buy_{name}"/>
            </div>"""
    data = data[:-24]
    if img % 4 == 0:
        data += """<div class="products">
        """
    else:
        data = data[:-11]
    data += a
    data += """
    </div>"""
    if img % 4 == 3:
        data += """
    <div class="space"></div>"""
    data += """
    </form>
    </body>"""
    print(data)
    file = open('html_css/buy_smth.html', mode='w', encoding='utf-8')
    file.write(data)
    file.close()


def add_money(nickname, money):
    # Подключение к БД
    con = sqlite3.connect("db/products.db")
    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    result = cur.execute(
        f"""Update user SET money = {money}
        WHERE nickname = '{nickname}'""")
    con.commit()
    con.close()


def get_money(nickname):
    con = sqlite3.connect("db/products.db")
    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    result = cur.execute(
        f"""Select money from user
            WHERE nickname = '{nickname}'""").fetchall()
    try:
        return result[0][0]
    except Exception:
        return 0


def my_thing(name, price, user, filename):
    file = open('html_css/my_things.html', mode='r', encoding='utf-8')
    u = file.read()
    file.close()
    data = u
    img = data.count('img')
    b = name.replace(' ', '_')
    b = b.replace(".", '_')
    a = f"""<div class="product_name">
                    <p class="txt" id="{name}">{name}: {price}RUB <span class="user">by {user}</span></p>
                    <img class="photo" src="css/images/{filename}">
                    <p class="txt2" id="am_{name}">Amount: <span style="font-size:30px">{{{{{b}}}}}</span></p>
</div>"""
    data = data[:-15]
    if img % 4 == 0:
        data += """<div class="products">
            """
    else:
        data = data[:-7]
    data += a
    data += """
</div>"""
    if img % 4 == 3:
        data += """
<div class="space"></div>"""
    data += """
</form>
</body>"""
    file = open('html_css/my_things.html', mode='w', encoding='utf-8')
    file.write(data)
    file.close()

def give_am(user, name):
    con = sqlite3.connect("db/products.db")
    cur = con.cursor()
    result = cur.execute(f"""Select amount from own WHERE name = '{name}' and user='{user}'""").fetchall()
    con.close()
    return result[0][0]


def all_products():
    con = sqlite3.connect("db/products.db")
    cur = con.cursor()
    result = cur.execute(f"""Select name from products""").fetchall()
    result = list(map(lambda x: x[0], result))
    return result

def get_user_name(prod):
    con = sqlite3.connect("db/products.db")
    cur = con.cursor()
    result = cur.execute(f"""Select user from products where name='{prod}'""").fetchall()
    return result[0][0]