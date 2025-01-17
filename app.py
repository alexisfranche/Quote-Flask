from flask import Flask, request , jsonify , render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)

# Database
ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:132456@localhost/quotes-flask'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ekaajrvphjkqjw:4747fb9f71d7d0313ed8854e5a3148d040d295e2d90df6ccf06072cdbe9f1294@ec2-107-21-209-1.compute-1.amazonaws.com:5432/dh25o76ojvfod'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

# Entry point
@app.route('/')
def index():
    return render_template('index.html')

# User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, username, password):
        self.username=username
        self.password=password

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')

# Init Schema User
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Create a user
@app.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    password = request.json['password']

    new_user = User(username, password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# Update a user
@app.route('/user/passID/<id>', methods=['PUT'])
def update_passwordByID(id):
    user = User.query.get(id)
    password = request.json['password']
    user.password = password
    db.session.commit()

    return user_schema.jsonify(user)

# Update a user by username
@app.route('/user/passName/<name>', methods=['PUT'])
def update_passwordByName(name):
    user = User.query.filter(User.username == name).first()
    password = request.json['password']
    user.password = password
    db.session.commit()

    return user_schema.jsonify(user)

# Delete user by id
@app.route('/user/delID/<id>', methods=['DELETE'])
def delete_userByID(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

# Delete user by name
@app.route('/user/delName/<name>', methods=['DELETE'])
def delete_userByName(name):
    user = User.query.filter(User.username == name).first()
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

# Get all users
@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Get single user by id
@app.route('/user/id/<id>', methods=['GET'])
def get_userById(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)  

# Get single user by username
@app.route('/user/name/<name>', methods=['GET'])
def get_userByName(name):
    user = User.query.filter(User.username == name).first()
    return user_schema.jsonify(user)  

# Quote Class/Model
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    content = db.Column(db.String(300))

    def __init__(self, author, content):
        self.author=author
        self.content=content


# Quote Schema
class QuoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'content')


# Init Schema quote
quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)

# Create a quote
@app.route('/quote', methods=['POST'])
def add_quote():
    author = request.json['author']
    content = request.json['content']

    new_quote = Quote(author, content)

    db.session.add(new_quote)
    db.session.commit()

    return quote_schema.jsonify(new_quote)

# Get all quotes
@app.route('/quote', methods=['GET'])
def get_quotes():
    all_quotes = Quote.query.all()
    result = quotes_schema.dump(all_quotes)
    return jsonify(result)

# Get single quote
@app.route('/quote/<id>', methods=['GET'])
def get_quote(id):
    quote = Quote.query.get(id)
    return quote_schema.jsonify(quote)

# Update a quote
@app.route('/quote/<id>', methods=['PUT'])
def update_quote(id):
    quote = Quote.query.get(id)

    author = request.json['author']
    content = request.json['content']

    quote.author = author
    quote.content = content

    db.session.commit()

    return quote_schema.jsonify(quote)

# Delete quote by id
@app.route('/quote/<id>', methods=['DELETE'])
def delete_quote(id):
    quote = Quote.query.get(id)
    db.session.delete(quote)
    db.session.commit()

    return quote_schema.jsonify(quote)

# This resets database when pushed to github,
# Once pushed in terminal do heroku run python then
# from app import db --> db.create_all() to init database
if ENV == 'dev':
    db.create_all()

# how to reset postgres db --> heroku restart --app quotes-flask and then heroku pg:reset DATABASE --app quotes-flask

# Run Server 
if __name__ == '__main__':
    app.run()
