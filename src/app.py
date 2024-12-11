"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Tags, ArticlesTags, Articles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


@app.route('/users', methods=['GET'])
def all_users():
    data = Users.query.all()
    data = [user.serialize() for user in data]
    return jsonify({"msg": "OK", "data": data})


@app.route('/tags', methods=['GET'])
def all_tags():
    data = Tags.query.all()
    data = [tag.serialize() for tag in data]
    return jsonify({"msg": "OK", "data": data})

@app.route('/articles', methods=['GET'])
def all_articles():
    articles = Articles.query.all()
    print('articleSSSSS',articles)
    articles = [article.serialize() for article in articles]
    return jsonify({"msg": "OK", "data": articles})



@app.route('/articles/<int:id>', methods=['GET'])
def one_article(id):
    article = Articles.query.get(id)
    print('article    ',article)
    return jsonify({"msg": "one article with id: " + str(id), "article": article.serialize()})


@app.route('/users', methods=['POST'])
def create_user():
    
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email or not password:
        return jsonify({"msg": 'todos los datos son necesarios'}), 400 
    check = Users.query.filter_by(email=email).first()
    if check:
        return jsonify({"msg": 'correo ya existem, inicia sesion'}), 400

    new_user = Users(email=email, password=password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "OK", "data": new_user.serialize()})

@app.route('/articles', methods=['POST'])
def create_article():
    
    title = request.json.get('title', None)
    content = request.json.get('content', None)
    user_id = request.json.get('user_id', None)
    
    if not title or not content or not user_id:
        return jsonify({"msg": 'todos los datos son necesarios'}), 400 
    
    data = Articles(title=title, content=content, user_id = user_id)
    db.session.add(data)
    db.session.commit()

    return jsonify({"msg": "OK", "data": data.sercontentialize()})


@app.route('/articles_tags', methods=['POST'])
def create_article_tags():
    article_id = request.json.get('article_id', None)
    tag_id = request.json.get('tag_id', None)
    extra_info = request.json.get('extra_info', None)
    if not article_id or not tag_id:
        return jsonify({"msg": 'todos los datos son necesarios'}), 400 
    
    data = ArticlesTags(article_id=article_id, tag_id=tag_id, extra_info= extra_info)
    db.session.add(data)
    db.session.commit()

    return jsonify({"msg": "OK", "data": data.serialize()})



@app.route('/articles/<int:id>', methods=['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({"msg": "deleted article with id: " + str(id)})



@app.route('/articles/<int:id>', methods=['PUT'])
def upd_article(id):
    title = request.json.get('title', None)
    content = request.json.get('content', None)
    
    article = Articles.query.get(id)
    if not article:
        return jsonify({"msg": "article not found"}), 404
    article.title = title or article.title
    if content:
        article.content = content

    db.session.commit()
    return jsonify({"msg": "updated article with id: " + str(id), "article": article.serialize()})




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
