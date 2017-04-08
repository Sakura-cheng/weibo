# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-03-14 16:35:16
# @Last Modified by:   wsljc
# @Last Modified time: 2017-04-08 19:52:21
from . import db
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Follow(db.Model):
	__tablename__ = 'follows'
	follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	#password = db.Column(db.String(64), nullable=False)
	password_hash = db.Column(db.String(128))
	articles = db.relationship('Article', backref='user')
	comments = db.relationship('Comment', backref='user')
	followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref=db.backref('followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
	followeds = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')

	def follow(self, user):
		if not self.is_following(user):
			f = Follow(follower=self, followed=user)

	def unfollow(self, user):
		f = self.followeds.filter_by(followed_id=user.id).first()
		if f:
			db.session.delete(f)

	def is_following(self, user):
		return self.followeds.filter_by(followed_id=user.id).first() is not None

	def is_followed_by(sefl, user):
		return self.followers.filter_by(follower_id=user.id).first() is not None

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

class Article(db.Model):
	__tablename__ = 'articles'
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(140), nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	comments = db.relationship('Comment', backref='article')

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))