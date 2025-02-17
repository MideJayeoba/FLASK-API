from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to suppress warnings
db = SQLAlchemy(app)
api = Api(app)  # You missed initializing the `Api` instance here

# Database model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"

# Argument parser for incoming requests
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Input a valid email please")

# Field marshalling for the response
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

# API Resource
class Users(Resource):
    def get(self):
        users = UserModel.query.all()
        return users, 200  # Status code for OK response

# Register the resource
api.add_resource(Users, '/api/users/')

# Home route
@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'



if __name__ == '__main__':
    app.run(debug=True)
