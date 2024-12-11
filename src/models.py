from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ArticlesTags(db.Model):
    __tablename__='articleTags'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    extra_info = db.Column(db.String(100))

    def __repr__(self):
        return '<ArticlesTags %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "article_id": self.article_id,
            "tag_id": self.tag_id,
            "extra_info": self.extra_info,
            # do not serialize the password, its a security breach
        }


class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    #               relationship('quien', backref='donde se muestra')
    articles = db.relationship('Articles', backref='user')



    def __repr__(self):
        return f"<User {self.email}>"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "articles": [article.serialize() for article in self.articles] if self.articles else None
            # do not serialize the password, its a security breach
        }

class Articles(db.Model):
    __tablename__='articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.relationship('Tags', secondary='articleTags', backref='articles') #devuelve lista



    def __repr__(self):
        return f"<Article {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "tags": [tag.serialize() for tag in self.tags] if self.tags else None
            # do not serialize the password, its a security breach
        }

class Tags(db.Model):
    __tablename__='tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(80), unique=False, nullable=False)
    #articles = db.relationship('Articles', backref='articlesTags')

    def __repr__(self):
        return '<Tags %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "tag": self.tag,
            # do not serialize the password, its a security breach
        }