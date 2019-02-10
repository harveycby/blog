from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin 

db = SQLAlchemy()

class User(db.Model,UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    
    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        """Python 风格的 getter """
        return self._password

    @password.setter
    def password(self, ori_password):
        """ Python 风格的 setter, 这样设置 user.password 就会自动为 password 生成哈希制存入 _password 字段 """
        self._password = generate_password_hash(ori_password)

    def check_password(self,password):
        """ 判断用户输入的密码和存储的 hash 密码是否相等 """
        return check_password_hash(self._password,password)
       

class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    title = db.Column(db.String(128), nullable=False)
    tags = db.Column(db.String(256), nullable=False)
    info = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.SmallInteger, default=1)
    isRecommand = db.Column(db.SmallInteger, default=1)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', uselist=False, backref=db.backref('blogs'))

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    name = db.Column(db.String(128), nullable=False)
    