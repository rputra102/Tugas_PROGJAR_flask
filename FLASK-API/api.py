from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    notelp = db.Column(db.Integer, unique=False, nullable=False)
    kota = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"User(name= {self.name}, email= {self.name}, notelp= {self.name}, kota= {self.name})"

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="nama gaboleh kosong")
user_args.add_argument('email', type=str, required=True, help="email gaboleh kosong")
user_args.add_argument('notelp', type=int, required=True, help="notelp gaboleh kosong")
user_args.add_argument('kota', type=str, required=True, help="kota gaboleh kosong")

userFields= {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'notelp': fields.Integer,
    'kota': fields.String,
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users= UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"], notelp=args["notelp"], kota=args["kota"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

    
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user= UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user
    
    @marshal_with(userFields)
    def patch(self, id):

        args = user_args.parse_args()
        user= UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        if args["name"]:
            user.name = args["name"]
        if args["email"]:
            user.email = args["email"]
        if args["notelp"] is not None:
            user.notelp = args["notelp"]
        if args["kota"]:
            user.kota = args["kota"]
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self, id):
        user= UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users
    
class NameFilter(Resource):
    @marshal_with(userFields)
    def get(self, name):
        user= UserModel.query.filter_by(name=name).first()
        if not user:
            abort(404, "User not found")
        return user
    
    @marshal_with(userFields)
    def patch(self, name):

        args = user_args.parse_args()
        user= UserModel.query.filter_by(name=name).first()
        if not user:
            abort(404, "User not found")
        if args["name"]:
            user.name = args["name"]
        if args["email"]:
            user.email = args["email"]
        if args["notelp"] is not None:
            user.notelp = args["notelp"]
        if args["kota"]:
            user.kota = args["kota"]
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self, name):
        user= UserModel.query.filter_by(name=name).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users

class EmailFilter(Resource):
    @marshal_with(userFields)
    def get(self, email):
        user= UserModel.query.filter_by(email=email).first()
        if not user:
            abort(404, "Email not found")
        return user
    
    @marshal_with(userFields)
    def patch(self, email):
        args = user_args.parse_args()
        user= UserModel.query.filter_by(email=email).first()
        if not user:
            abort(404, "Email not found")
        user.name = args["name"]
        user.name = args["email"]
        user.name = args["notelp"]
        user.name = args["kota"]
        db.session.commit()
        return user, 201, {"message":"Email updated"}
    
    @marshal_with(userFields)
    def delete(self, email):
        user= UserModel.query.filter_by(email=email).first()
        if not user:
            abort(404, "Email not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users

api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/id/<int:id>')
api.add_resource(NameFilter, '/api/users/name/<string:name>')
api.add_resource(EmailFilter, '/api/users/email/<string:email>')

@app.route('/')
def home():
    return '<h1>KELOMPOK PROGJAR</h1>'

if __name__ == '__main__':
    app.run(debug=True)