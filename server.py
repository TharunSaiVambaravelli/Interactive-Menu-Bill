from flask import Flask, request, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from sqlalchemy import desc
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user, current_user, logout_user, login_required, UserMixin
'''This is app python file'''
app = Flask(__name__)
DATABSE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root', password='tharun7675', server='localhost', database='ssd')

app.config['SESSION_TYPE'] = "sqlalchemy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['SQLALCHEMY_DATABASE_URI'] = DATABSE_URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:81426@localhost/ssd'


app.config['SECRET_KEY'] = 'secretKey'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

user_details = {}


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    transaction_id = db.relationship('Transaction', backref='user')
    name = db.Column(db.String(80), nullable=False)
    pwd = db.Column(db.String(80), nullable=False)
    is_chef = db.Column(db.Integer, default=False, nullable=False)

    def __init__(self, _id, name, pwd, is_chef):
        self.id = _id
        self.name = name
        self.pwd = pwd
        self.is_chef = is_chef


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # order_id=db.relationship('Orders')
    half_price = db.Column(db.Integer, nullable=False)
    full_price = db.Column(db.Integer, nullable=False)

    def __init__(self, _id, half_price, full_price):
        self.id = _id
        self.half_price = half_price
        self.full_price = full_price


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    plate_type = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    # price=db.Column(db.Integer,nullable=False)

    trans_id = db.Column(db.Integer, db.ForeignKey('transaction.t_id'))

    def __init__(self, item_id, plate_type, quantity, trans_id):
        # self.order_id=_id
        self.item_id = item_id
        self.plate_type = plate_type
        self.quantity = quantity
        # self.price=price
        self.trans_id = trans_id


class Transaction(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    t_id = db.Column(db.Integer, nullable=False, primary_key=True)
    tip = db.Column(db.String(80), nullable=False)  # tip is in percentge
    discount = db.Column(
        db.FLOAT(
            precision=32,
            decimal_return_scale=None))  # is in val
    share_bill = db.Column(db.Integer, nullable=False)
    total = db.Column(
        db.FLOAT(
            precision=32,
            decimal_return_scale=None),
        nullable=False)
    play_game = db.Column(db.Integer, nullable=False)

    def __init__(self, _id, tip, discount, share_bill, total, play_game):
        self.user_id = _id
        # self.t_id=t_id
        self.tip = tip
        self.discount = discount
        self.share_bill = share_bill
        self.total = total
        self.play_game = play_game


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup', methods=['POST'])
def create():
    '''
        create() function is used for creating a user
    '''
    data = request.get_json()
    check_id = User.query.filter_by(id=data['id']).first()

    if check_id:
        return "User already Exists"

    new_user = User(data['id'], data['name'], data['pwd'], data['is_chef'])
    db.session.add(new_user)
    db.session.commit()

    return "User added sucessfully."


@app.route('/delete/<int:_id>', methods=['DELETE'])
def delete(_id):

    return "Delete success"


@app.route('/logout', methods=['PUT'])
def logout():
    logout_user()
    return "logged out"


@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    id = data['id']
    pwd = data['password']
    check_id = User.query.filter_by(id=data['id']).first()

    if check_id is None:
        return "User does'nt exists"

    if check_id.pwd != pwd:
        return "Incorrect Password"

    user_details['is_chef'] = check_id.is_chef
    login_user(check_id)

    return "LoggedIn"


@app.route('/addmenu', methods=['POST'])
def add_menu():
    '''
        add_menu() function is used for adding a food item
    '''
    data = request.get_json()
    check_id = Menu.query.filter_by(id=data['item_id']).first()

    if check_id is None:

        M = Menu(
            data['item_id'],
            data['half_plate_price'],
            data['full_plate_price'])

        if(user_details['is_chef']):

            db.session.add(M)
            db.session.commit()

            return "Menu Item added successfully"
        else:
            return "user is not a chef"

    else:
        return "Item id already exists"


@app.route('/readmenu', methods=['GET'])
def readmenu():
    '''
        readmenu() function is used for reading current menu
    '''
    menu = Menu.query.all()
    response = {}
    for i in menu:
        response[i.id] = {'half_plate': i.half_price,
                          'full_plate': i.full_price}

    return jsonify(response)


@app.route('/addtrans', methods=['POST'])
def addtrans():

    data = request.get_json()

    # _id,tip,discount,share_bill,total,play_game

    new_user = Transaction(
        data['_id'],
        data['tip'],
        data['discount'],
        data['share_bill'],
        data["total"],
        data["play_game"])
    db.session.add(new_user)
    db.session.commit()
    print(new_user.t_id)
    # data["half_plates"] data["full_plates"]
    print(data['full_plates'], data['half_plates'])
    half_plates = data['half_plates']
    full_plates = data['full_plates']
    for i in half_plates:
        new_order = Orders(i, "half", half_plates[i], new_user.t_id)
        db.session.add(new_order)
        db.session.commit()
        
    for i in full_plates:
        new_order = Orders(i, "full", full_plates[i], new_user.t_id)
        db.session.add(new_order)
        db.session.commit()

    #  check_id=User.query.filter_by(id=data['id']).first()
    return "Trans added sucessfully."


@app.route('/checkchef', methods=['POST'])
def checkchef():
    data = request.get_json()
    obj = User.query.filter_by(id=data['id']).first()
    if obj.is_chef == 1:
        return "1"
    return "0"


@app.route('/showtids', methods=['POST'])
def showtids():
    l1 = []
    data = request.get_json()
    check_id = Transaction.query.filter_by(user_id=data['user_id'])
    for i in check_id:
        l1.append(i.t_id)
    print(l1)
    return jsonify(l1)



@app.route('/gettransd', methods=['POST'])
def gettransd():
    check_id = Orders.query.filter_by(trans_id=data['t_id']).first()
    l=[]
    #tip, discount, share_bill, total, play_game
    l.append(check_id.tip)
    l.append(check_id.discount)
    l.append(check_id.share_bill)
    l.append(check_id.total)
    l.append(check_id.play_game)
    return jsonify((l))



@app.route('/getorder', methods=['POST'])
def getorder():
    
    temp = {}
    data = request.get_json()
    check_id = Orders.query.filter_by(trans_id=data['t_id'])
    for i in check_id:
        # item_id,plate_type,quantity,trans_id
        l1 = []
        if i.plate_type == "half":
            l1.append({"half": i.quantity})
            # temp[i.item_id]=
            # l["half"]=i.quantity

        if i.plate_type == "full":
            l1.append({"full": i.quantity})
            # temp[i.item_id]={"full":i.quantity}

        temp[i.item_id] = l1

    print((temp))

    return jsonify(temp)


if __name__ == '__main__':
    #db.drop_all()
    db.create_all()
    app.run(port=8000, debug=True)
    print(create.__doc__)
    print(add_menu.__doc__)
    print(readmenu.__doc__)
