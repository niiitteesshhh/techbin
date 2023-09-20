from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import jwt
import uuid
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bin:bin@localhost:3306/techbin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from Models.admin_model import Admin
from Models.user_model import User
from Models.record_model import Record
from Models.trashcan_model import Trashcan
from Models.user_pincode_model import User_pincode


@app.route("/")
def home():
    return {"success": "true"}


@app.route("/admin_login", methods=['POST'])
def login():
    creds = request.get_json()
    username = creds['username']
    password = creds['password']
    admin = Admin.query.filter(Admin.username == username).first()
    if admin is None:
        return {"message": "Invalid Credentials"}
    hashed = bcrypt.checkpw(password.encode(), admin.password.encode())
    if hashed:
        newjwt = jwt.encode({"uuid": admin.uuid}, "secret", algorithm="HS256")
        response = make_response({"message": "login successful"})
        response.set_cookie('jwt', newjwt)
        return response
    else:
        return {"message": "Invalid Credentials"}


@app.route("/admin_register", methods=['POST'])
def admin_register():
    creds = request.get_json()
    username = creds['username']
    password = creds['password']
    name = creds['name']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    newuuid = uuid.uuid4().hex
    admin = Admin(username=username, password=hashed, uuid=newuuid, name=name)
    db.session.add(admin)
    db.session.commit()
    return {"message": "admin registered"}


@app.route("/user_register", methods=['POST'])
def user_register():
    creds = request.get_json()
    username = creds['username']
    password = creds['password']
    name = creds['name']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    newuuid = uuid.uuid4().hex
    user = User(username=username, password=hashed, uuid=newuuid, name=name)
    db.session.add(user)
    db.session.commit()
    return {"message": "user registered"}


@app.route("/user_login", methods=['POST'])
def user_login():
    creds = request.get_json()
    username = creds['username']
    password = creds['password']
    user = User.query.filter(User.username == username).first()
    if user is None:
        return {"message": "Invalid Credentials"}
    hashed = bcrypt.checkpw(password.encode(), user.password.encode())
    if hashed:
        newjwt = jwt.encode({"uuid": user.uuid}, "secret", algorithm="HS256")
        response = make_response({"message": "login successful"})
        response.set_cookie('jwt', newjwt)
        return response
    else:
        return {"message": "Invalid Credentials"}


@app.route("/trashcan/<int:trashcan_id>/status", methods=['PUT'])
def changestatus(trashcan_id):
    status = request.get_json()['status']
    trashcan = Trashcan.query.filter(Trashcan.id == trashcan_id).first()
    trashcan.status = status
    db.session.commit()
    return {"message": "status changed"}


@app.route("/trashcan/<int:trashcan_id>/record", methods=['GET'])
def getrecord(trashcan_id):
    trashcan = Trashcan.query.filter(Trashcan.id == trashcan_id).first()
    records = Record.query.filter(Record.trashcan_id == trashcan.id).all()
    response = {"records": []}
    for record in records:
        user = User.query.filter(User.id == record.user_id).first()
        response["records"].append({"id": record.id, "trashcan_id": record.trashcan_id,
                                    "user_id": record.user_id, "username": user.username, "lastPickup": record.lastPickup})
    return response


@app.route("/trashcan/<int:trashcan_id>/record", methods=['POST'])
def addrecord(trashcan_id):
    creds = request.get_json()
    user_id = creds['user_id']
    trashcan = Trashcan.query.filter(Trashcan.id == trashcan_id).first()
    record = Record(trashcan_id=trashcan_id, user_id=user_id)
    db.session.add(record)
    db.session.commit()
    return {"message": "record added"}


@app.route("/getalltrashcans/<string:pincode>", methods=['GET'])
def getalltrashcans(pincode):
    trashcans = Trashcan.query.filter(Trashcan.pincode == pincode).all()
    response = {"trashcans": []}
    for trashcan in trashcans:
        response["trashcans"].append({"id": trashcan.id, "pincode": trashcan.pincode,
                                        "status": trashcan.status, "latitude": trashcan.latitude, "longitude": trashcan.longitude})
    return response

@app.route("/getallpincodes", methods=['GET'])
def getallpincodes():
    distinct_pincodes = User_pincode.query.distinct(User_pincode.pincode).all()
    response = {"pincodes": []}
    for pincode in distinct_pincodes:
        response["pincodes"].append({"id": pincode.id, "pincode": pincode.pincode})
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
