# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-03-11 18:21:39
# @Last Modified by:   wsljc
# @Last Modified time: 2017-05-07 14:13:48
import os
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, jsonify, send_from_directory

from . import main
from .forms import PublishForm, LoginForm, RegisterForm, CommentForm#, ModifyForm
from .. import db, photos
from ..models import User, Comment, Article, Follow, Like
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
path = './weibo/static/images/touxiang'
sensitive_table = ['习近平', '毛泽东', '江泽民', '法轮功', '屌', '屄', '操你妈']

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET', 'POST'])
def index():
	articles = Article.query.order_by(Article.timestamp.desc()).all()
	who = current_user._get_current_object()
	form = PublishForm()
	loginform = LoginForm()
	registerform = RegisterForm()
	if form.validate_on_submit():
		for item in sensitive_table:
			if item in form.content.data:
				flash('铭感字符；' + item)
				return redirect(url_for('.index'))
		article = Article(
			content=form.content.data, 
			user=current_user._get_current_object()
			)
		db.session.add(article)
		return redirect(url_for('.index'))
	return render_template('index.html', current_time=datetime.utcnow(), form=form, loginform=loginform, registerform=registerform, articles=articles)

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

@main.route('/login_content/<article_id>', methods=['GET', 'POST'])
def login_content(article_id):
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(request.args.get('next') or url_for('.content', article_id=article_id))
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
		return redirect(url_for('.index'))
	return render_template(url_for('.index'), form=form)

@main.route('/content/<article_id>', methods=['GET', 'POST'])
def content(article_id):
	loginform = LoginForm()
	registerform = RegisterForm()
	commentform = CommentForm()
	article = Article.query.filter_by(id=article_id).first()
	n = article.id
	if commentform.validate_on_submit():
		comment = Comment(
			content=commentform.content.data, 
			user=current_user._get_current_object(), 
			article_id=n
			)
		db.session.add(comment)
		db.session.execute('UPDATE articles SET comments_number = comments_number + 1 WHERE id = %d' % n)
	comments =Comment.query.filter_by(article_id=article_id)
	total = Article.query.filter_by(user_id=article.user.id).count()
	return render_template('content.html', article=article, total=total, comments=comments, loginform=loginform, registerform=registerform, commentform=commentform)

@main.route('/about/<username>', methods=['GET', 'POST'])
@login_required
def about(username):
	loginform = LoginForm()
	registerform = RegisterForm()
	# modifyform = ModifyForm()
	user = User.query.filter_by(username=username).first()
	user_id = user.id
	if request.method == 'POST':
		username = request.form['username']
		content = request.form['message']
		db.session.execute("UPDATE users SET username = '%s' WHERE id = %d" % (username, user_id))
		db.session.execute("UPDATE users SET content = '%s' WHERE id = %d" % (content, user_id))
		return redirect(url_for('.about', username=username))
	return render_template('aboutme.html', loginform=loginform, registerform=registerform)

@main.route('/<username>', methods=['GET', 'POST'])
#@login_required
def usercenter(username, x=0):
	loginform = LoginForm()
	registerform = RegisterForm()
	x = request.args.get('x', 0)
	user = User.query.filter_by(username=username).first()
	articles = Article.query.filter_by(user_id=user.id).order_by(Article.timestamp.desc()).all()
	total = Article.query.filter_by(user_id=user.id).count()
	return render_template('userpage.html', articles=articles, total=total, user=user, loginform=loginform, registerform=registerform, func = x)

@main.route('/like/<article_id>', methods=['GET', 'POST'])
@login_required
def like(article_id):
	article = Article.query.filter_by(id=article_id).first()
	n = article.id
	like = Like(
		content = 1, 
		user=current_user._get_current_object(), 
		article_id=n
		)
	db.session.add(like)
	db.session.execute("UPDATE articles SET like_number = like_number + 1 WHERE id = %d" % n)
	return jsonify(result=article.like_number+1)

@main.route('/unlike/<article_id>', methods=['GET', 'POST'])
@login_required
def unlike(article_id):
	article = Article.query.filter_by(id=article_id).first()
	n = article.id
	like = Like.query.filter_by(article_id=n).first()
	m = like.id
	db.session.execute('DELETE FROM likes WHERE id = %d' % m)
	db.session.execute("UPDATE articles SET like_number = like_number - 1 WHERE id = %d" % n)
	return jsonify(result=article.like_number-1)

@main.route('/follow/<username>', methods=['GET', 'POST'])
@login_required
def follow_from_index(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('用户不存在')
		return redirect(url_for('.index'))
	#if current_user.is_following(user):
	#	flash('你已经关注Ta了')
	#	return redirect(url_for('.index'))
	current_user.follow(user)
	#flash('你现在已关注Ta了')
	return jsonify(result='取关')

@main.route('/unfollow/<username>', methods=['GET', 'POST'])
@login_required
def unfollow_from_index(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('用户不存在')
		return redirect(url_for('.index'))
	current_user.unfollow(user)
	#flash('你现在已取关Ta了')
	return jsonify(result='关注')

@main.route('/upload_file/<filename>')
def uploaded_file(filename):
	return send_from_directory(path, filename)

@main.route('/upload/<username>', methods=['GET', 'POST'])
def upload_file(username):
	user = User.query.filter_by(username=username).first()
	n = user.id
	loginform = LoginForm()
	registerform = RegisterForm()
	username = username
	if request.method == 'POST' and 'file' in request.files:
		file = request.files['file']
		if file:
			# image_path = '..\\static\\images\\touxiang\\' + username + '.jpg'
			# print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
			# if os.path.exists(image_path):
			# 	print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
			# 	os.unlink(image_path)
			filename = photos.save(file, name=str(n) + '.jpg')
			db.session.execute("UPDATE users SET image = '%s' WHERE id = %d" % (filename, n))
			return redirect(url_for('.about', username=username))
		else:
			return redirect(url_for('.about', username=username))
		# file = request.files['file']
		# if file and allowed_file(file.filename):
		# 	filename = username
		# 	db.session.execute("UPDATE users SET image = '%s' WHERE id = %d" % (filename, n))
		# 	filename = filename + '.jpg'
		# 	file.save(os.path.join(path, filename))
		# 	return redirect(url_for('.about', username=username))
		# else:
		# 	filename = None
	else:
		filename = None
	return render_template('aboutme.html', loginform=loginform, registerform=registerform, filename=filename)
	# if form.validate_on_submit():
	# 	filename = photos.save(request.files['file'])
	# 	filename = filename[:-4]
	# 	db.session.execute("UPDATE users SET image = '%s' WHERE id = %d" % (filename, n))
	# 	return redirect(url_for('.about', username=username))
	# else:
	# 	filename = None
	# return render_template('aboutme.html', form=form, loginform=loginform, registerform=registerform, filename=filename)

# ---------------------------------------------------------------------------

@main.route('/unfollow_/<username>', methods=['GET', 'POST'])
@login_required
def unfollow_(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('用户不存在')
		return redirect(url_for('.index'))
	current_user.unfollow(user)
	flash('你现在已取关Ta了')
	return redirect(url_for('.usercenter', username=current_user._get_current_object().username, x=1))

@main.route('/unfollow__/<username>', methods=['GET', 'POST'])
@login_required
def unfollow__(username):
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