# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-03-11 18:21:39
# @Last Modified by:   wsljc
# @Last Modified time: 2017-04-09 11:40:24
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash

from . import main
from .forms import PublishForm, LoginForm, RegisterForm
from .. import db
from ..models import User, Comment, Article, Follow
from flask_login import login_required, login_user, logout_user, current_user

@main.route('/', methods=['GET', 'POST'])
def index():
	articles = Article.query.order_by(Article.timestamp.desc()).all()
	form = PublishForm()
	if form.validate_on_submit():
		article = Article(
			content=form.content.data, 
			user=current_user._get_current_object()
			)
		db.session.add(article)
		return redirect(url_for('.index'))
	return render_template('index.html', current_time=datetime.utcnow(), form=form, articles=articles)

@main.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('无效的用户名或密码')
	return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(
			email=form.email.data, 
			username=form.username.data, 
			password=form.password.data
			)
		db.session.add(user)
		#db.session.commit()
		flash('你现在可以登录了')
		return redirect(url_for('.login'))
	return render_template('register.html', form=form)

@main.route('/<username>', methods=['GET', 'POST'])
@login_required
def usercenter(username):
	user = User.query.filter_by(username=username).first()
	articles = Article.query.filter_by(user_id=user.id).order_by(Article.timestamp.desc()).all()
	total = Article.query.filter_by(user_id=user.id).count()
	return render_template('usercenter.html', articles=articles, total=total, user=user)

@main.route('/follow/<username>')
@login_required
def follow_from_index(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('用户不存在')
		return redirect(url_for('.index'))
	if current_user.is_following(user):
		flash('你已经关注Ta了')
		return redirect(url_for('.index'))
	current_user.follow(user)
	flash('你现在已关注Ta了')
	return redirect(url_for('.index'))

@main.route('/unfollow/<username>')
@login_required
def unfollow_from_index(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('用户不存在')
		return redirect(url_for('.index'))
	current_user.unfollow(user)
	flash('你现在已取关Ta了')
	return redirect(url_for('.index'))

@main.route('/logout')
@login_required
def logout():
	logout_user()
	flash('你已退出')
	return redirect(url_for('main.index'))